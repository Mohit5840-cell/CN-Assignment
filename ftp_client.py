from ftplib import FTP

def ftp_client():
    ftp = FTP("ftp.dlptest.com")  # Public test FTP server
    ftp.login(user="dlpuser", passwd="rNrKYTX9g7z3RgJRmxWuGHbeu")

    print("=== Directory Listing ===")
    ftp.retrlines("LIST")

    # Upload file
    filename = "upload_test.txt"
    with open(filename, "w") as f:
        f.write("This is a test file uploaded via FTP.")
    with open(filename, "rb") as f:
        ftp.storbinary(f"STOR {filename}", f)
    print(f"Uploaded {filename} successfully.")

    # Download file
    with open("download_test.txt", "wb") as f:
        ftp.retrbinary("RETR " + filename, f.write)
    print("Downloaded file successfully.")

    ftp.quit()

if __name__ == "__main__":
    ftp_client()
