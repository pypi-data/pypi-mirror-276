import argparse
import email
import html
import sys
from bs4 import BeautifulSoup, Doctype
import css_inline


def main():
    """
    Create an Outlook-style HTML reply
    """

    # Parse args
    parser = argparse.ArgumentParser(description="Create an Outlook-style HTML reply")
    parser.add_argument("-m", "--message",
                        nargs='?',
                        type=argparse.FileType('r'),
                        help="Original message file")
    parser.add_argument("-r", "--reply",
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="HTML reply, file or defaults to stdin")
    parser.add_argument("-o", "--output",
                        nargs='?',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help="HTML output, file or defaults to stdout")

    args = parser.parse_args()

    # Get the reply html from file/stdin
    html_reply = args.reply.read()

    # Get the original headers and html from the original email (rfc822 format)
    rfc822_original = email.message_from_file(args.message)
    html_original_msg = _get_message_html(rfc822_original)
    html_original_headers = _get_header_html(rfc822_original)

    # Convert HTML text to BeautifulSoup object and inline all CSS

    ## reply
    bs4_msg = BeautifulSoup(css_inline.inline(html_reply),'html.parser')

    ## message
    bs4_original_msg = BeautifulSoup(css_inline.inline(html_original_msg), 'html.parser')
    bs4_original_msg.html.unwrap() #type: ignore
    bs4_original_msg.body.unwrap() #type: ignore
    bs4_original_msg.head.extract() #type: ignore
    for element in bs4_original_msg.contents:
        if isinstance(element, Doctype):
            element.extract()

    ## headers
    bs4_original_headers = BeautifulSoup(html_original_headers, 'html.parser')

    # Combine converted HTML together
    bs4_final = bs4_msg
    bs4_final.body.append(BeautifulSoup('<hr></hr>', 'html.parser')) #type: ignore
    bs4_final.body.append(bs4_original_headers) #type: ignore
    bs4_final.body.append(bs4_original_msg) #type: ignore

    # Write output
    args.output.write(str(bs4_final))


def _get_header_html(message):
    headers = ''
    if message['from'] is not None:
        headers = '<b>From</b>: ' + html.escape(message['from']) + '<br></br>'
    if message['date'] is not None:
        headers = headers + '<b>Date</b>: ' + html.escape(message['date']) + '<br></br>'
    if message['to'] is not None:
        headers = headers + '<b>To</b>: ' + html.escape(message['to']) + '<br></br>'
    if message['cc'] is not None:
        headers = headers + '<b>Cc</b>: ' + html.escape(message['cc']) + '<br></br>'
    if message['subject'] is not None:
        headers = headers + '<b>Subject</b>: ' + html.escape(message['subject']) + '<br></br>'
    return headers


def _get_message_html(message):
    body = None
    if message.is_multipart():
        for part in message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/html' and 'attachment' not in cdispo:
                body = part.get_payload()
                break
    else:
        body = message.get_payload()

    if body is not None:
        return str(body)
    else:
        raise ValueError

if __name__ == "__main__":
    main()
