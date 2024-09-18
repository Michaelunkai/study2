import qrcode

def generate_qr(url, output_file):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(output_file)
    print(f"QR code generated and saved as {output_file}")

if __name__ == "__main__":
    url = input("Enter the URL: ")
    output_file = "url_qr.png"
    generate_qr(url, output_file)
