from time import sleep


class SteamLogin:
    too_many_tries = "There have been too many login failures from your network in a short time period.  Please wait and try again later."
    wrong_pass = "Le nom de compte ou mot de passe saisi est incorrect."

    def __init__(self, browser):
        self.browser = browser

    def login(self, user, password):
        self.browser.get('https://steamcommunity.com/login/home/')

        username = self.browser.find_element_by_name("username")
        pw = self.browser.find_element_by_name("password")
        send = self.browser.find_element_by_id("SteamLogin")

        username.send_keys(user)
        pw.send_keys(password)
        if self.check_captcha():
            print(f"Please solve the captcha (Please do not sign in)")
            user_in = "n"
            while user_in.lower() != "y":
                user_in = input("Are you done solving? (y/n): ")
        send.click()

        sleep(2.0)
        error_code = self.login_status()
        if error_code is not None:
            if error_code == 0xE01:
                print(f"The password {password} for user {user} is wrong.")
            elif error_code == 0xE02:
                print("Try again later.")
            return False

        sleep(2.0)
        if self.check_two_factor():
            steam_guard = input("Please enter your 2FA code: ")
            steam_guard_input = self.browser.find_element_by_id("twofactorcode_entry")
            steam_guard_input.send_keys(steam_guard)
            sg_button = self.browser.find_elements_by_xpath("//div[@id='login_twofactorauth_buttonset_entercode']/div[@type='submit']")
            sg_button[0].click()

        sleep(5.0)
        return True

    def login_status(self):
        res = self.browser.find_element_by_id("error_display").text
        if res == SteamLogin.wrong_pass:
            return 0xE01
        elif res == SteamLogin.too_many_tries:
            return 0xE02
        return None

    def check_captcha(self):
        return len(self.browser.find_element_by_id("captchaExplanation").text) > 0

    def check_two_factor(self):
        steam_guard = self.browser.find_element_by_id("login_twofactorauth_icon")
        return len(str(steam_guard)) > 0

