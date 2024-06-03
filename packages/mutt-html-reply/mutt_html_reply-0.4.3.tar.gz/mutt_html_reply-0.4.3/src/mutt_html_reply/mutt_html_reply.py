import argparse
import datetime
from zoneinfo import ZoneInfo
import email
from email.header import decode_header
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
    parser.add_argument("-z", "--zoneinfo",
                        nargs='?',
                        type=str,
                        default="America/New_York",
                        help="ZoneInfo for header display, defaults to 'America/New_York'")

    args = parser.parse_args()

    # Get the reply html from file/stdin
    html_reply = args.reply.read()

    # Get the original headers and html from the original email (rfc822 format)
    rfc822_original = email.message_from_file(args.message)
    html_original_msg = _get_message_html(rfc822_original)
    html_original_headers = _get_header_html(rfc822_original, args.zoneinfo)

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
    bs4_final.body.append(BeautifulSoup('<br></br>', 'html.parser')) #type: ignore
    bs4_final.body.append(bs4_original_msg) #type: ignore

    # Write output
    args.output.write(str(bs4_final))


def _get_header_html(message, tz_str):
    headers = '''\
        <div>
        <div style=&quot;border:none;border-top:solid;padding:3.0pt 0in 0in 0in&quot;>
        <span style=font-size:11.0pt;font-family:&quot;Calibri&quot;,sans-serif>
        '''
    if message['from'] is not None:
        headers = headers + '<b>From:</b> ' + html.escape(message['from'].replace('"','')) + '<br></br>'
    if message['date'] is not None:
        # Try to make it pretty
        try:
            header_date = datetime.datetime.strptime(html.escape(message['date'].replace('"','')),'%a, %d %b %Y %H:%M:%S%z').astimezone(ZoneInfo(tz_str))
            header_date = str(header_date.strftime('%A, %B %d, %Y %I:%M %p'))
        except:
            pass
        try:
            header_date = datetime.datetime.strptime(html.escape(message['date'].replace('"','')),'%a, %d %b %Y %H:%M:%S %z').astimezone(ZoneInfo("America/New_York"))
            header_date = str(header_date.strftime('%A, %B %d, %Y %I:%M %p'))
        except:
            header_date = message['date']
        headers = headers + '<b>Sent:</b> ' + header_date +'<br></br>'
    if message['to'] is not None:
        headers = headers + '<b>To:</b> ' + html.escape(message['to'].replace('"','')) + '<br></br>'
    if message['cc'] is not None:
        headers = headers + '<b>Cc:</b> ' + html.escape(message['cc'].replace('"','')) + '<br></br>'
    if message['subject'] is not None:
        decoded_subject_list = decode_header(message['subject'])
        first_subject_line = decoded_subject_list[0]
        try:
            decoded_subject = first_subject_line[0].decode(first_subject_line[1])
            headers = headers + '<b>Subject:</b> ' + html.escape(decoded_subject) + '<br></br>'
        except:
            headers = headers + '<b>Subject:</b> ' + html.escape(message['subject']) + '<br></br>'

    headers = headers + '''\
        </span>
        </div>
        </div>
        '''


    return headers

def _get_message_html(message):
    body = ''
    first_part = True
    for part in message.walk():
        ctype = part.get_content_type()
        cdispo = str(part.get('Content-Disposition'))
        cte = str(part.get('Content-Transfer-Encoding'))
        charsets = part.get_charsets()
        if ctype == 'text/html' and 'attachment' not in cdispo:
            if charsets is not None:
                for charset in charsets:
                    try:
                        if charset == 'utf-8' and 'quoted-printable' not in cte and 'base64' not in cte:
                            needs_decode = False
                        else:
                            needs_decode = True
                        if needs_decode:
                            if first_part:
                                body = part.get_payload(decode=needs_decode).decode(charset)
                            else:
                                body = body + part.get_payload(decode=needs_decode).decode(charset)
                        else:
                            if first_part:
                                body = part.get_payload(decode=needs_decode)
                            else:
                                body = body + part.get_payload(decode=needs_decode)
                    except:
                        continue

    return body


if __name__ == "__main__":
    main()
