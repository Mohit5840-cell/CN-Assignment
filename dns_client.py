import dns.resolver
import logging

# ---------- Logging Setup ----------
logging.basicConfig(
    filename="dns_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def resolve_dns(domain):
    try:
        logging.info(f"Resolving DNS for domain: {domain}")
        print(f"Resolving DNS for {domain}\n")

        # 1. Resolve IP address (A record)
        try:
            answers = dns.resolver.resolve(domain, "A")
            for rdata in answers:
                result = f"A record (IP): {rdata.address}"
                print(result)
                logging.info(result)
        except Exception as e:
            logging.warning(f"No A record found: {e}")

        # 2. Resolve MX records
        try:
            answers = dns.resolver.resolve(domain, "MX")
            for rdata in answers:
                result = f"MX record: {rdata.exchange} (priority {rdata.preference})"
                print(result)
                logging.info(result)
        except Exception as e:
            logging.warning(f"No MX record found: {e}")

        # 3. Resolve CNAME records
        try:
            answers = dns.resolver.resolve(domain, "CNAME")
            for rdata in answers:
                result = f"CNAME record: {rdata.target}"
                print(result)
                logging.info(result)
        except Exception as e:
            logging.warning(f"No CNAME record found: {e}")

    except Exception as e:
        print("Error:", e)
        logging.error("Error occurred: " + str(e))

if __name__ == "__main__":
    # Example domain (you can change it)
    resolve_dns("example.com")
    resolve_dns("gmail.com")

