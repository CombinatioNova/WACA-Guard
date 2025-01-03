# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import abc
import logging
import re
from dataclasses import dataclass
from enum import Enum

import aiohttp

from socialscan import __version__


class QueryError(Exception):
    pass


class UsernameQueryable(metaclass=abc.ABCMeta):
    """Abstract class for platforms that can query usernames."""

    @abc.abstractmethod
    async def check_username(self, username):
        raise NotImplementedError


class EmailQueryable(metaclass=abc.ABCMeta):
    """Abstract class for platforms that can query email addresses."""

    @abc.abstractmethod
    async def check_email(self, email):
        raise NotImplementedError


class PrerequestRequired(metaclass=abc.ABCMeta):
    """Abstract class for platforms that require a pre-request to retrieve a token,
    for use in the main query. This request is sent once and cached for future
    queries."""

    @abc.abstractmethod
    async def prerequest(self):
        raise NotImplementedError

    async def get_token(self):
        """
        Retrieve and return platform token using the `prerequest` method specified in the class

        Normal calls will not be able to take advantage of this as all tokens are retrieved concurrently
        This only applies to when tokens are retrieved before main queries with -c
        Adds 1-2s to overall running time but halves HTTP requests sent for bulk queries
        """
        if self.prerequest_sent:
            if self.token is None:
                raise QueryError(BasePlatform.TOKEN_ERROR_MESSAGE)
            return self.token
        else:
            self.token = await self.prerequest()
            self.prerequest_sent = True
            if self.token is None:
                raise QueryError(BasePlatform.TOKEN_ERROR_MESSAGE)
            logging.debug(f"TOKEN {Platforms(self.__class__)}: {self.token}")
            return self.token


class BasePlatform:
    # Default user agent taken from `odeialba/instagram-php-scraper`
    # https://github.com/odeialba/instagram-php-scraper/blob/39e8565e8446fa2c66dbcdee8807aa03fca2bbda/src/InstagramScraper/Instagram.php#L46
    DEFAULT_HEADERS = {
        "User-agent": "Mozilla/5.0 (Linux; Android 8.1.0; motorola one Build/OPKS28.63-18-3; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 Instagram 72.0.0.21.98 Android (27/8.1.0; 320dpi; 720x1362; motorola; motorola one; deen_sprout; qcom; pt_BR; 132081645)",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    }
    UNEXPECTED_CONTENT_TYPE_ERROR_MESSAGE = "Unexpected content type {}. You might be sending too many requests. Use a proxy or wait before trying again."
    TOKEN_ERROR_MESSAGE = "Could not retrieve token. You might be sending too many requests. Use a proxy or wait before trying again."
    TOO_MANY_REQUEST_ERROR_MESSAGE = "Requests denied by platform due to excessive requests. Use a proxy or wait before trying again."
    TIMEOUT_DURATION = 15

    client_timeout = aiohttp.ClientTimeout(connect=TIMEOUT_DURATION)

    # 1: Be as explicit as possible in handling all cases
    # 2: Do not include any queries that will lead to side-effects on users (e.g. submitting sign up forms)
    # OK to omit checks for whether a key exists when parsing the JSON response. KeyError is handled by the parent coroutine.

    def response_failure(self, query, *, message="Failure"):
        return PlatformResponse(
            platform=Platforms(self.__class__),
            query=query,
            available=False,
            valid=False,
            success=False,
            message=message,
            link=None,
        )

    def response_available(self, query, *, message="Available"):
        return PlatformResponse(
            platform=Platforms(self.__class__),
            query=query,
            available=True,
            valid=True,
            success=True,
            message=message,
            link=None,
        )

    def response_unavailable(self, query, *, message="Unavailable", link=None):
        return PlatformResponse(
            platform=Platforms(self.__class__),
            query=query,
            available=False,
            valid=True,
            success=True,
            message=message,
            link=link,
        )

    def response_invalid(self, query, *, message="Invalid"):
        return PlatformResponse(
            platform=Platforms(self.__class__),
            query=query,
            available=False,
            valid=False,
            success=True,
            message=message,
            link=None,
        )

    def response_unavailable_or_invalid(self, query, *, message, unavailable_messages, link=None):
        if any(x in message for x in unavailable_messages):
            return self.response_unavailable(query, message=message, link=link)
        else:
            return self.response_invalid(query, message=message)

    def _request(self, method, url, **kwargs):
        proxy = (
            self.proxy_list[self.request_count % len(self.proxy_list)] if self.proxy_list else None
        )
        self.request_count += 1
        if "headers" in kwargs:
            kwargs["headers"].update(BasePlatform.DEFAULT_HEADERS)
        else:
            kwargs["headers"] = BasePlatform.DEFAULT_HEADERS
        return self.session.request(method, url, timeout=self.client_timeout, proxy=proxy, **kwargs)

    def post(self, url, **kwargs):
        logging.debug(f"POST {url}")
        return self._request("POST", url, **kwargs)

    def get(self, url, **kwargs):
        logging.debug(f"GET {url}")
        return self._request("GET", url, **kwargs)

    @staticmethod
    async def get_json(request):
        if not request.headers["Content-Type"].startswith("application/json"):
            raise QueryError(
                BasePlatform.UNEXPECTED_CONTENT_TYPE_ERROR_MESSAGE.format(
                    request.headers["Content-Type"]
                )
            )
        else:
            json = await request.json()
            logging.debug(f"JSON {request.url} {request.status}: {json}")
            return json

    @staticmethod
    async def get_text(request):
        text = await request.text()
        logging.debug(f"TEXT {request.url} {request.status}: {text}")
        return text

    def __init__(self, session, proxy_list=[]):
        self.session = session
        self.proxy_list = proxy_list
        self.request_count = 0
        self.prerequest_sent = False
        self.token = None


class Snapchat(BasePlatform, UsernameQueryable, PrerequestRequired):
    URL = "https://accounts.snapchat.com/accounts/login"
    ENDPOINT = "https://accounts.snapchat.com/accounts/get_username_suggestions"
    USERNAME_TAKEN_MSGS = ["is already taken", "is currently unavailable"]

    async def prerequest(self):
        async with self.get(Snapchat.URL) as r:
            """
            See: https://github.com/aio-libs/aiohttp/issues/3002
            Snapchat sends multiple Set-Cookie headers in its response setting the value of 'xsrf-token',
            causing the original value of 'xsrf-token' to be overwritten in aiohttp
            Need to analyse the header response to extract the required value
            """
            cookies = r.headers.getall("Set-Cookie")
            for cookie in cookies:
                match = re.search(r"xsrf_token=([\w-]*);", cookie)
                if match:
                    token = match.group(1)
                    return token

    async def check_username(self, username):
        token = await self.get_token()
        async with self.post(
            Snapchat.ENDPOINT,
            data={"requested_username": username, "xsrf_token": token},
            cookies={"xsrf_token": token},
        ) as r:
            # Non-JSON received if too many requests
            json_body = await self.get_json(r)
            if "error_message" in json_body["value"]:
                return self.response_unavailable_or_invalid(
                    username,
                    message=json_body["value"]["error_message"],
                    unavailable_messages=Snapchat.USERNAME_TAKEN_MSGS,
                )
            elif json_body["value"]["status_code"] == "OK":
                return self.response_available(username)

    # Email: Snapchat doesn't associate email addresses with accounts


class Instagram(BasePlatform, UsernameQueryable, EmailQueryable, PrerequestRequired):
    URL = "https://www.instagram.com/api/v1/public/landing_info/"
    ENDPOINT = "https://www.instagram.com/accounts/web_create_ajax/attempt/"
    USERNAME_TAKEN_MSGS = [
        "This username isn't available.",
        "A user with that username already exists.",
    ]
    USERNAME_LINK_FORMAT = "https://www.instagram.com/{}"

    async def prerequest(self):
        async with self.get(Instagram.URL) as r:
            if "csrftoken" in r.cookies:
                token = r.cookies["csrftoken"].value
                return token

    async def check_username(self, username):
        token = await self.get_token()
        async with self.post(
            Instagram.ENDPOINT, data={"username": username}, headers={"x-csrftoken": token}
        ) as r:
            json_body = await self.get_json(r)
            # Too many requests
            if json_body["status"] == "fail":
                return self.response_failure(username, message=json_body["message"])
            if "username" in json_body["errors"]:
                return self.response_unavailable_or_invalid(
                    username,
                    message=json_body["errors"]["username"][0]["message"],
                    unavailable_messages=Instagram.USERNAME_TAKEN_MSGS,
                    link=Instagram.USERNAME_LINK_FORMAT.format(username),
                )
            else:
                return self.response_available(username)

    async def check_email(self, email):
        token = await self.get_token()
        async with self.post(
            Instagram.ENDPOINT, data={"email": email}, headers={"x-csrftoken": token}
        ) as r:
            json_body = await self.get_json(r)
            # Too many requests
            if json_body["status"] == "fail":
                return self.response_failure(email, message=json_body["message"])
            if "email" not in json_body["errors"]:
                return self.response_available(email)
            else:
                message = json_body["errors"]["email"][0]["message"]
                if json_body["errors"]["email"][0]["code"] == "invalid_email":
                    return self.response_invalid(email, message=message)
                else:
                    return self.response_unavailable(email, message=message)


class GitHub(BasePlatform, UsernameQueryable, EmailQueryable, PrerequestRequired):
    URL = "https://github.com/join"
    USERNAME_ENDPOINT = "https://github.com/signup_check/username"
    EMAIL_ENDPOINT = "https://github.com/signup_check/email"
    # [username taken, reserved keyword (Username __ is unavailable)]
    USERNAME_TAKEN_MSGS = ["already taken", "unavailable", "not available"]
    USERNAME_LINK_FORMAT = "https://github.com/{}"

    token_regex = re.compile(
        r'<auto-check src="/signup_check/username[\s\S]*?value="([\S]+)"[\s\S]*<auto-check src="/signup_check/email[\s\S]*?value="([\S]+)"'
    )
    tag_regex = re.compile(r"<[^>]+>")

    async def prerequest(self):
        async with self.get(GitHub.URL) as r:
            text = await self.get_text(r)
            match = self.token_regex.search(text)
            if match:
                username_token = match.group(1)
                email_token = match.group(2)
                return (username_token, email_token)

    async def check_username(self, username):
        pr = await self.get_token()
        (username_token, _) = pr
        async with self.post(
            GitHub.USERNAME_ENDPOINT,
            data={"value": username, "authenticity_token": username_token},
        ) as r:
            if r.status == 422:
                text = await self.get_text(r)
                text = self.tag_regex.sub("", text).strip()
                return self.response_unavailable_or_invalid(
                    username,
                    message=text,
                    unavailable_messages=GitHub.USERNAME_TAKEN_MSGS,
                    link=GitHub.USERNAME_LINK_FORMAT.format(username),
                )
            elif r.status == 200:
                return self.response_available(username)
            elif r.status == 429:
                return self.response_failure(
                    username, message=BasePlatform.TOO_MANY_REQUEST_ERROR_MESSAGE
                )

    async def check_email(self, email):
        pr = await self.get_token()
        if pr is None:
            return self.response_failure(email, message=BasePlatform.TOKEN_ERROR_MESSAGE)
        else:
            (_, email_token) = pr
        async with self.post(
            GitHub.EMAIL_ENDPOINT,
            data={"value": email, "authenticity_token": email_token},
        ) as r:
            if r.status == 422:
                text = await self.get_text(r)
                return self.response_unavailable(email, message=text)
            elif r.status == 200:
                return self.response_available(email)
            elif r.status == 429:
                return self.response_failure(
                    email, message=BasePlatform.TOO_MANY_REQUEST_ERROR_MESSAGE
                )


class Tumblr(BasePlatform, UsernameQueryable, EmailQueryable, PrerequestRequired):
    URL = "https://tumblr.com/register"
    ENDPOINT = "https://www.tumblr.com/api/v2/register/account/validate"
    USERNAME_LINK_FORMAT = "https://{}.tumblr.com"

    SAMPLE_UNUSED_EMAIL = "akc2rW33AuSqQWY8@gmail.com"
    SAMPLE_PASSWORD = "correcthorsebatterystaple"
    SAMPLE_UNUSED_USERNAME = "akc2rW33AuSqQWY8"

    async def prerequest(self):
        async with self.get(Tumblr.URL) as r:
            text = await self.get_text(r)
            match = re.search(r'"API_TOKEN":"([\s\S]+?)"', text)
            if match:
                token = match.group(1)
                return token

    async def _check(self, email=SAMPLE_UNUSED_EMAIL, username=SAMPLE_UNUSED_USERNAME):
        query = email if username == Tumblr.SAMPLE_UNUSED_USERNAME else username
        token = await self.get_token()
        async with self.post(
            Tumblr.ENDPOINT,
            json={
                "email": email,
                "tumblelog": username,
                "password": Tumblr.SAMPLE_PASSWORD,
            },
            headers={
                "authorization": f"Bearer {token}",
            },
        ) as r:
            json_body = await self.get_json(r)
            if "error" in json_body["response"] and "code" in json_body["response"]:
                if json_body["response"]["code"] == 3 and username == query:
                    return self.response_unavailable(
                        username,
                        message=json_body["response"]["error"],
                        link=Tumblr.USERNAME_LINK_FORMAT.format(query),
                    )
                elif json_body["response"]["code"] == 2 and email == query:
                    return self.response_unavailable(
                        email,
                        message=json_body["response"]["error"],
                        link=Tumblr.USERNAME_LINK_FORMAT.format(query),
                    )
                else:
                    return self.response_invalid(query, message=json_body["response"]["error"])
            elif json_body["meta"]["status"] == 200:
                return self.response_available(query)
            else:
                return self.response_failure(query, message="Unknown response")

    async def check_username(self, username):
        return await self._check(username=username)

    async def check_email(self, email):
        return await self._check(email=email)


class GitLab(BasePlatform, UsernameQueryable):
    URL = "https://gitlab.com/users/sign_in"
    ENDPOINT = "https://gitlab.com/users/{}/exists"
    USERNAME_LINK_FORMAT = "https://gitlab.com/{}"

    async def check_username(self, username):
        # Custom matching required as validation is implemented locally and not server-side by GitLab
        if not re.fullmatch(
            r"[a-zA-Z0-9_\.][a-zA-Z0-9_\-\.]*[a-zA-Z0-9_\-]|[a-zA-Z0-9_]", username
        ):
            return self.response_invalid(
                username, message="Please create a username with only alphanumeric characters."
            )
        async with self.get(
            GitLab.ENDPOINT.format(username), headers={"X-Requested-With": "XMLHttpRequest"}
        ) as r:
            # Special case for usernames
            if r.status == 401:
                return self.response_unavailable(
                    username, link=GitLab.USERNAME_LINK_FORMAT.format(username)
                )
            json_body = await self.get_json(r)
            if json_body["exists"]:
                return self.response_unavailable(
                    username, link=GitLab.USERNAME_LINK_FORMAT.format(username)
                )
            else:
                return self.response_available(username)

    # Email: GitLab requires a reCAPTCHA token to check email address usage which we cannot bypass


class Reddit(BasePlatform, UsernameQueryable):
    URL = "https://reddit.com"
    ENDPOINT = "https://www.reddit.com/api/check_username.json"
    USERNAME_TAKEN_MSGS = [
        "that username is already taken",
        "that username is taken by a deleted account",
    ]
    USERNAME_LINK_FORMAT = "https://www.reddit.com/u/{}"

    async def check_username(self, username):
        # Custom user agent required to overcome rate limits for Reddit API
        async with self.post(Reddit.ENDPOINT, data={"user": username}) as r:
            json_body = await self.get_json(r)
            if "error" in json_body and json_body["error"] == 429:
                return self.response_failure(
                    username, message=BasePlatform.TOO_MANY_REQUEST_ERROR_MESSAGE
                )
            elif "json" in json_body:
                return self.response_unavailable_or_invalid(
                    username,
                    message=json_body["json"]["errors"][0][1],
                    unavailable_messages=Reddit.USERNAME_TAKEN_MSGS,
                    link=Reddit.USERNAME_LINK_FORMAT.format(username),
                )
            elif json_body == {}:
                return self.response_available(username)

    # Email: You can register multiple Reddit accounts under the same email address so not possible to check if an address is in use


class Twitter(BasePlatform, UsernameQueryable, EmailQueryable):
    URL = "https://twitter.com/signup"
    USERNAME_ENDPOINT = "https://api.twitter.com/i/users/username_available.json"
    EMAIL_ENDPOINT = "https://api.twitter.com/i/users/email_available.json"
    # [account in use, account suspended]
    USERNAME_TAKEN_MSGS = ["That username has been taken", "unavailable"]
    USERNAME_LINK_FORMAT = "https://twitter.com/{}"

    async def check_username(self, username):
        async with self.get(Twitter.USERNAME_ENDPOINT, params={"username": username}) as r:
            json_body = await self.get_json(r)
            message = json_body["desc"]
            if json_body["valid"]:
                return self.response_available(username, message=message)
            else:
                return self.response_unavailable_or_invalid(
                    username,
                    message=message,
                    unavailable_messages=Twitter.USERNAME_TAKEN_MSGS,
                    link=Twitter.USERNAME_LINK_FORMAT.format(username),
                )

    async def check_email(self, email):
        async with self.get(Twitter.EMAIL_ENDPOINT, params={"email": email}) as r:
            json_body = await self.get_json(r)
            message = json_body["msg"]
            if not json_body["valid"] and not json_body["taken"]:
                return self.response_invalid(email, message=message)

            if json_body["taken"]:
                return self.response_unavailable(email, message=message)
            else:
                return self.response_available(email, message=message)


class Pinterest(BasePlatform, EmailQueryable):
    URL = "https://www.pinterest.com"
    EMAIL_ENDPOINT = "https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/"

    async def check_email(self, email):
        data = '{"options": {"email": "%s"}, "context": {}}' % email
        async with self.get(
            Pinterest.EMAIL_ENDPOINT, params={"source_url": "/", "data": data}
        ) as r:
            json_body = await self.get_json(r)
            email_exists = json_body["resource_response"]["data"]
            if email_exists:
                return self.response_unavailable(email)
            else:
                return self.response_available(email)


class Lastfm(BasePlatform, UsernameQueryable, EmailQueryable, PrerequestRequired):
    URL = "https://www.last.fm/join"
    ENDPOINT = "https://www.last.fm/join/partial/validate"
    USERNAME_TAKEN_MSGS = ["Sorry, this username isn't available."]
    USERNAME_LINK_FORMAT = "https://www.last.fm/user/{}"

    async def prerequest(self):
        async with self.get(Lastfm.URL) as r:
            if "csrftoken" in r.cookies:
                token = r.cookies["csrftoken"].value
                return token

    async def _check(self, username="", email=""):
        token = await self.get_token()
        data = {"csrfmiddlewaretoken": token, "userName": username, "email": email}
        headers = {
            "Accept": "*/*",
            "Referer": "https://www.last.fm/join",
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": f"csrftoken={token}",
        }
        async with self.post(Lastfm.ENDPOINT, data=data, headers=headers) as r:
            json_body = await self.get_json(r)
            if email:
                if json_body["email"]["valid"]:
                    return self.response_available(
                        email, message=json_body["email"]["success_message"]
                    )
                else:
                    return self.response_unavailable(
                        email, message=json_body["email"]["error_messages"][0]
                    )
            elif username:
                if json_body["userName"]["valid"]:
                    return self.response_available(
                        username, message=json_body["userName"]["success_message"]
                    )
                else:
                    return self.response_unavailable_or_invalid(
                        username,
                        message=re.sub("<[^<]+?>", "", json_body["userName"]["error_messages"][0]),
                        unavailable_messages=Lastfm.USERNAME_TAKEN_MSGS,
                        link=Lastfm.USERNAME_LINK_FORMAT.format(username),
                    )

    async def check_email(self, email):
        return await self._check(email=email)

    async def check_username(self, username):
        return await self._check(username=username)


class Yahoo(BasePlatform, UsernameQueryable, PrerequestRequired):
    URL = "https://login.yahoo.com/account/create"
    USERNAME_ENDPOINT = "https://login.yahoo.com/account/module/create?validateField=yid"

    # Modified from Yahoo source
    error_messages = {
        "IDENTIFIER_EXISTS": "A Yahoo account already exists with this email address. REPLACE_SIGNIN_LINK.",
        "DANGLING_IDENTIFIER_EXISTS": "A Yahoo account already exists with this email address.",
        "IDENTIFIER_NOT_AVAILABLE": "This email address is not available for sign up, try something else",
        "EMAIL_DOMAIN_NOT_ALLOWED": "You cannot use this email address. Instead try creating Yahoo email address",
        "RESERVED_WORD_PRESENT": "A Yahoo account already exists with this email address.",
        "SOME_SPECIAL_CHARACTERS_NOT_ALLOWED": "You can only use letters, numbers, periods (‘.’), and underscores (‘_’) in your username.",
        "SOME_SPECIAL_CHARACTERS_NOT_ALLOWED_IN_EMAIL": "Make sure you use your full email address, including an “@” sign and a domain.",
        "INVALID_IDENTIFIER": "Error: Invalid identifier.",
        "CANNOT_END_WITH_SPECIAL_CHARACTER": "Your username has to end with a letter or a number.",
        "CANNOT_HAVE_MORE_THAN_ONE_PERIOD": "You can’t have more than one ‘.’ in your username.",
        "NEED_AT_LEAST_ONE_ALPHA": "Please use at least one letter in your username.",
        "CANNOT_START_WITH_SPECIAL_CHARACTER_OR_NUMBER": "Your username has to start with a letter.",
        "CONSECUTIVE_SPECIAL_CHARACTERS_NOT_ALLOWED": "You can’t have more than one ‘.’ or ‘_’ in a row.",
        "INVALID_NAME_LENGTH": "That name is too long.",
        "LENGTH_TOO_SHORT": "That email address is too short, please use a longer one.",
        "LENGTH_TOO_LONG": "That email address is too long, please use a shorter one.",
        "NAME_CONTAINS_URL": "You can't use this name",
        "ELECTION_SPECIFIC_WORD_PRESENT": "Not available, try something else.",
    }

    regex = re.compile(r"v=1&s=([^\s]*)")

    async def prerequest(self):
        async with self.get(Yahoo.URL) as r:
            if "AS" in r.cookies:
                match = self.regex.search(r.cookies["AS"].value)
                if match:
                    return match.group(1)

    async def check_username(self, username):
        token = await self.get_token()
        async with self.post(
            Yahoo.USERNAME_ENDPOINT,
            data={"specId": "yidReg", "acrumb": token, "yid": username},
            headers={"X-Requested-With": "XMLHttpRequest"},
        ) as r:
            json_body = await self.get_json(r)
            if json_body["errors"][2]["name"] != "yid":
                return self.response_available(username)
            else:
                error = json_body["errors"][2]["error"]
                error_pretty = self.error_messages.get(error, error.replace("_", " ").capitalize())
                if error in (
                    "IDENTIFIER_EXISTS",
                    "RESERVED_WORD_PRESENT",
                    "IDENTIFIER_NOT_AVAILABLE",
                    "DANGLING_IDENTIFIER_EXISTS",
                ):
                    return self.response_unavailable(username, message=error_pretty)
                else:
                    return self.response_invalid(username, message=error_pretty)


class Firefox(BasePlatform, EmailQueryable):
    URL = "https://accounts.firefox.com/signup"
    EMAIL_ENDPOINT = "https://api.accounts.firefox.com/v1/account/status"

    async def check_email(self, email):
        async with self.post(Firefox.EMAIL_ENDPOINT, data={"email": email}) as r:
            json_body = await self.get_json(r)
            if "error" in json_body:
                return self.response_failure(email, message=json_body["message"])
            elif json_body["exists"]:
                return self.response_unavailable(email)
            else:
                return self.response_available(email)


class Platforms(Enum):
    GITHUB = GitHub
    GITLAB = GitLab
    INSTAGRAM = Instagram
    PINTEREST = Pinterest
    REDDIT = Reddit
    TWITTER = Twitter
    TUMBLR = Tumblr
    FIREFOX = Firefox
    SNAPCHAT = Snapchat
    YAHOO = Yahoo
    LASTFM = Lastfm

    def __str__(self):
        return self.value.__name__

    def __len__(self):
        return len(self.value.__name__)


@dataclass(frozen=True)
class PlatformResponse:
    platform: Platforms
    query: str
    available: bool
    valid: bool
    success: bool
    message: str
    link: str
