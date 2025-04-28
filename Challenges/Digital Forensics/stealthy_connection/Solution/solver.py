## solver you need to craft this script to retrive the chunks of the zip file from the dns pkts and then crack the zip file with rockyou

import pyshark


DOMAIN = "securinets.tn"  
CHUNK_SIZE = 8  

def xor_bytes(data, key):
    return bytes([b ^ key for b in data])

def decode_dns_query(qname):
    parts = qname.split(".")
    if len(parts) < 3:
        return None, None  
    
    try:
        key = int(parts[0], 16)  
        encoded_data = ''.join(parts[1])  

        decoded_data = bytes.fromhex(encoded_data)
        
        return key, decoded_data
    except Exception as e:
        print(f"Error decoding query {qname}: {e}")
        return None, None

def extract_dns_exfiltration(pcapng_file):

    extracted_data = bytearray()

    cap = pyshark.FileCapture(pcapng_file, display_filter="dns")
    for pkt in cap:
        if hasattr(pkt, 'dns') and hasattr(pkt.dns, 'qry_name'):
            qname = pkt.dns.qry_name
            src_ip = pkt.ip.src
            if DOMAIN in qname and (src_ip == "192.168.100.5"):  
                print(f"Found DNS query: {qname}")
                
                key, decoded_chunk = decode_dns_query(qname)
                if key is not None:
                    original_chunk = xor_bytes(decoded_chunk, key)
                    extracted_data.extend(original_chunk)
    
    return extracted_data

def reconstruct_file(extracted_data, output_file="reconstructed.zip"):
    with open(output_file, "wb") as f:
        f.write(extracted_data)
    print(f"Reconstructed file saved to {output_file}")

def main():
    pcapng_file = "chall.pcapng"  
    extracted_data = extract_dns_exfiltration(pcapng_file)
    
    if extracted_data:
        print(f"[+] Successfully extracted {len(extracted_data)} bytes of data")
        reconstruct_file(extracted_data)
    else:
        print("[-] No DNS exfiltration data found.")

if __name__ == "__main__":
    main()
