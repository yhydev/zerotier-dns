import requests
import argparse
import logging

def put_records(apikey, zone, name, addresses):
    headers = {
                "Authorization": "Bearer " + apikey
            }
    url = "https://api.cloudflare.com/client/v4/zones/%s/dns_records" % zone
    resp_json = requests.get(url, params={
            "type": "A",
            "name": name
        },headers=headers).json()
    logging.info("records: %s", resp_json)
    for record in resp_json['result']:
        if record['content'] not in addresses:
            requests.delete(url + "/" + record['id'], headers = headers)
        else:
            addresses.remove(record['content'])
    for address in addresses:
        resp_json = requests.post(url, json={
                "type": "A",
                "name": name,
                "content": address,
                "ttl":60
            },headers=headers)
        logging.info("put_record: %s", resp_json.json())

def get_zerotier_member_addresses(token, network_id):
    url = "https://api.zerotier.com/api/v1/network/%s/member" % network_id
    members = requests.get(url, headers={
        "authorization": "token %s" % token
    }).json()
    return [member['config']['ipAssignments'][0] for member in members]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ap = argparse.ArgumentParser()
    ap.add_argument("--zt-token", required=True, type=str)
    ap.add_argument("--zt-net-id", required=True, type=str)
    ap.add_argument("--cf-api-key", required=True, type=str)
    ap.add_argument("--cf-zone-id", required=True, type=str)
    ap.add_argument("--cf-name", required=True, type=str)
    args = ap.parse_args()
    addresses = get_zerotier_member_addresses(args.zt_token, args.zt_net_id)
    put_records(
        args.cf_api_key,
        args.cf_zone_id,
        args.cf_name,
        addresses
        )
