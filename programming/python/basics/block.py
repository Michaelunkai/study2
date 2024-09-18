from mitmproxy import http

class AdsBlocker:
    def __init__(self):
        self.ad_domains = [
            "ad.doubleclick.net",
            "googleads.g.doubleclick.net",
            "ads.youtube.com",
            # Add more ad domains as needed
        ]

    def request(self, flow: http.HTTPFlow) -> None:
        for domain in self.ad_domains:
            if domain in flow.request.pretty_url:
                flow.response = http.HTTPResponse.make(200)  # Return a blank response
                print(f"Blocked request to {domain}")

addons = [
    AdsBlocker()
]
