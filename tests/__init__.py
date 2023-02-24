class HelperOutputCases:
    def case_default(self):
        return "username=GITHUB_NAME\npassword=GITHUB_TOKEN\n"

    def case_space_delimited(self):
        return "username = GITHUB_NAME\npassword = GITHUB_TOKEN\n"

    def case_additional_empty_line(self):
        return "username=GITHUB_NAME\n\npassword=GITHUB_TOKEN\n"

    def case_additional_non_empty_line(self):
        return "username=GITHUB_NAME\n# comment\npassword=GITHUB_TOKEN\n"
