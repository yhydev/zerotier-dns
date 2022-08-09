import requests
import argparse
import logging
from requests_html import HTMLSession
import zerotier_dns

def get_gatevpn_address():
    html = HTMLSession().get("https://www.vpngate.net/cn/", headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }).html
    return html.xpath('//tr/td[2]/span[1]/text()')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ap = argparse.ArgumentParser()
    ap.add_argument("--cf-api-key", required=True, type=str)
    ap.add_argument("--cf-zone-id", required=True, type=str)
    ap.add_argument("--cf-name", required=True, type=str)
    args = ap.parse_args()
    addresses = get_gatevpn_address()
    zerotier_dns.put_records(
        args.cf_api_key,
        args.cf_zone_id,
        args.cf_name,
        addresses
        )