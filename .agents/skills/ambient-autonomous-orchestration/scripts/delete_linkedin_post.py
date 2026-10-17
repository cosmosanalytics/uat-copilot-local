import sys
import requests
import urllib.parse

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'

def delete_post(urn):
    encoded_urn = urllib.parse.quote(urn)
    url = f"https://api.linkedin.com/v2/ugcPosts/{encoded_urn}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    print(f"Attempting to delete LinkedIn post: {urn}...")
    res = requests.delete(url, headers=headers)
    print("Status code:", res.status_code)
    if res.status_code in (200, 204):
        print(f"SUCCESS: Post {urn} deleted successfully.")
    else:
        print(f"Response: {res.text}")

if __name__ == "__main__":
    target_urn = sys.argv[1] if len(sys.argv) > 1 else "urn:li:share:7517273680062820354"
    delete_post(target_urn)
