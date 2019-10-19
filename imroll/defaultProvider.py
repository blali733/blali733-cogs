import datetime


class DefaultProvider:

    def get_strings(self):
        return {
            "disabled_info": ["I am out of order, sorry ;("],
            "no_response": ["Server gave no response."],
            "m1": ["As requested by: {}"],
            "m2": ["{}: {}"],
            "request_error": ["Error during request processing. Exception raised in line: {}"],
            "no_result": ["Cannot find an image that can be viewed by you."],
            "filter_add": ["Filter '{}' added to the server's {} filter list."],
            "filter_exists": ["Filter '{}' is already in the server's {} filter list."],
            "filter_max": ["This server has exceeded the maximum filters ({}/{})."],
            "filter_del": ["Filter '{}' deleted from the server's {} filter list."],
            "filter_not_existing": ["Filter '{}' does not exist in the server's {} filter list."],
            "filter_revert": ["Reverted the server to the default {} filter list."],
            "filter_default": ["Server is already using the default {} filter list."],
            "filter_list": ["{} filter list: ```\n{}```"],
            "filter_no_custom": ["No custom filters found!"],
            "filter_found": ["{} filters not found!"],
            "filter_no_module": ["{} module not found!"],
            "sth_disabled": ["{} - disabled!"],
            "sth_enabled": ["{} - enabled!"],
            "GTFO": ["You are banned!"],
            "ban_given": ["You are banned for next {} day(s)"],
            "ban_evaded": ["Your reputation lets you avoid punishment."],
            "stats_empty": ["No statistics for this server."],
            "stats_overall": ["Since {}, following users rolled: ```\n👑{}```"],
            "stats_daily": ["{}: ```\n👑{}```"],
        }

    def get_filters(self):
        return {"default": {"loli": ["rating:safe"], "gel": ["rating:safe"], "dan": ["rating:safe"],
                            "kona": ["rating:safe"]}}

    def get_settings(self):
        return {"maxfilters": {"loli": "50", "gel": "10", "dan": "50", "kona": "50"}}

    def get_active(self):
        return {
            "current": {
                "dan": "true",
                "gel": "true",
                "kona": "true",
                "loli": "true"
            },
            "killed": "False"
        }

    def get_counter(self):
        now = datetime.datetime.now()
        date = "{}.{}.{}".format(now.day, now.month, now.year)
        return {"default": {"date": date}}

    def get_bans(self):
        return {"default": {"ban": {}, "whitelist": [], "rules": {"daily": "50", "VACation": "7"}}}
