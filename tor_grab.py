

import os, ssl, urllib.parse, urllib.request
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup


html2 = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <title>The Pirate Bay - The galaxy's most resilient bittorrent site</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Search The Pirate Bay" />
    <link rel="stylesheet" type="text/css" href="//pirateproxy.llc/static/css/pirate6.css"/>
    
    
    
    
    
    
    
    
    
    <link rel="canonical" href="//pirateproxy.llc/search/jeopardy/0/3/0" />
    <style type="text/css">
        .searchBox{
            margin: 6px;
            width: 300px;
            vertical-align: middle;
            padding: 2px;
            background-image:url('//pirateproxy.llc/static/img/icon-https.gif');
            background-repeat:no-repeat;
            background-position: right;
        }
        .detLink {
            font-size: 1.2em;
            font-weight: 400;
        }
        .detDesc {
            color: #4e5456;
        }
        .detDesc a:hover {
            color: #000099;
            text-decoration: underline;
        }
        .sortby {
            text-align: left;
            float: left;
        }
        .detName {
            padding-top: 3px;
            padding-bottom: 2px;
        }
        .viewswitch {
            font-style: normal;
            float: right;
            text-align: right;
            font-weight: normal;
        }
    </style>
    <script src="//pirateproxy.llc/static/js/jquery.min.js" type="text/javascript"></script>
    <script src="//pirateproxy.llc/static/js/tpb.js" type="text/javascript"></script>
    <meta name="description" content="Search for and download any torrent from the pirate bay using search query jeopardy. Direct download via magnet link."/>
    <meta name="keywords" content="jeopardy direct download torrent magnet tpb piratebay search"/>

    <script language="javascript" type="text/javascript">if (top.location != self.location) {top.location.replace(self.location);}</script>
<script data-cfasync="false" type="text/javascript">eval(window.atob("dmFyIGFkY2FzaE1hY3Jvcz17c3ViMToiIixzdWIyOiIifSx6b25lU2V0dD17cjoiMTkxMjQyMyJ9LHVybHM9e2NkblVybHM6WyIvL2NlbGVyaXRhc2Nkbi5jb20iLCIvL2NvbW1lcmNpYWx2YWx1ZS5vcmciXSxjZG5JbmRleDowLHJhbmQ6TWF0aC5yYW5kb20oKSxldmVudHM6WyJjbGljayIsIm1vdXNlZG93biIsInRvdWNoc3RhcnQiXSx1c2VGaXhlcjohMCxvbmx5Rml4ZXI6ITEsZml4ZXJCZW5lYXRoOiExfSxfMHhiMTcwPVsibyAyaSgxZCl7OCAxZj1xLlgoXCIyY1wiKTs4IEY7cyh0IHEuRiE9PScxMicpe0Y9cS5GfTFle0Y9cS4yOCgnRicpWzBdfTFmLjFZPVwiMmstMnJcIjsxZi4xbz0xZDtGLjFxKDFmKTs4IFk9cS5YKFwiMmNcIik7WS4xWT1cIllcIjtZLjFvPTFkO0YuMXEoWSl9OCBWPVEgbygpezggdz11OzggMjk9Sy5UKCk7OCAxTD0yejs4IDFHPTJSO3UuMTM9eycyUCc6aiwnMlEnOmosJzJWJzpqLCcyVyc6aiwnMzEnOmosJzMwJzpqLCcyWic6aiwnMlgnOmosJzJZJzpqLCcyTyc6aiwnMkYnOmosJzJEJzpqLCcyQyc6aiwnMkEnOmosJzJHJzpqfTt1LjFnPVEgbygpezggej11O3ouMWE9RDt1LjJmPW8oKXs4IHg9cS5YKCcxYicpO3guMjcoXCIyNS0yNlwiLEQpO3guMjA9Jy8vMkguMkwuMlQvMkovMXQvMkkuMXQnOzggTD0odCBwLkc9PT0nQScpP3AuRzpEOzggMTE9KHQgcC5IPT09J0EnKT9wLkg6RDtzKEw9PT1qJiYxMT09PWope3guMjQ9bygpe3ouMWE9ajt6LkgoKX19cyhMPT09RCl7eC4ySz14LjJNPW8oKXsxdigpfX04IHk9dy4xcygpO3kuMWguMjMoeCx5KX07dS5IPW8oKXtzKHQgcS4xeCE9PScxMicmJnEuMXghPT0yQil7ei4xYygpfTFlezFsKHouSCwyRSl9fTt1LjFjPW8oKXtzKHQgMXkuciE9PScxUycpe0J9cygxeS5yLko8NSl7Qn1FLjFsKG8oKXtzKHouMWE9PT1qKXs4IGw9MCxkPVEoRS4yTnx8RS4yU3x8RS4yVSkoezMyOlt7MWQ6XCIybToycDoyb1wifV19LHsyeTpbezJ3OiEwfV19KTtkLjJxPW8oYil7OCBlPVwiXCI7IWIuTXx8KGIuTSYmYi5NLk0uMU4oJzJ2Jyk9PS0xKXx8IShiPS8oWzAtOV17MSwzfShcXC5bMC05XXsxLDN9KXszfXxbYS0xOS05XXsxLDR9KDpbYS0xOS05XXsxLDR9KXs3fSkvLjJ1KGIuTS5NKVsxXSl8fG18fGIuVygvXigydFxcLjJzXFwufDJ4XFwuMmpcXC58MTBcXC58MmxcXC4oMVs2LTldfDJcXGR8M1sybl0pKS8pfHxiLlcoL15bYS0xOS05XXsxLDR9KDpbYS0xOS05XXsxLDR9KXs3fSQvKXx8KG09ITAsZT1iLHEuM3A9bygpezF1PTFIKChxLlIuVyhcIjFWPShbXjtdLis/KSg7fCQpXCIpfHxbXSlbMV18fDApO3MoIWwmJjFMPjF1JiYhKChxLlIuVyhcIjFJPShbXjtdLis/KSg7fCQpXCIpfHxbXSlbMV18fDApKXtsPTE7OCAxaT1LLjFNKDFLKksuVCgpKSxmPUsuVCgpLjFCKDM2KS4xRCgvW15hLTFFLTFGLTldKy9nLFwiXCIpLjFKKDAsMTApOzggUD1cIjNxOi8vXCIrZStcIi9cIituLjJnKDFpK1wiL1wiKygxSCgxeS5yKSsxaSkrXCIvXCIrZik7cyh0IEk9PT0ndicmJnQgVi4xMz09PSd2Jyl7Wig4IEMgM28gSSl7cyhJLjNuKEMpKXtzKHQgSVtDXT09PScxUycmJklbQ10hPT0nJyYmSVtDXS5KPjApe3ModCBWLjEzW0NdPT09J0EnJiZWLjEzW0NdPT09ail7UD1QKyhQLjFOKCc/Jyk+MD8nJic6Jz8nKStDKyc9JyszcyhJW0NdKX19fX19OCBhPXEuWChcImFcIiksYj1LLjFNKDFLKksuVCgpKTthLjFvPSh0IHAuMTY9PT0nQScmJnAuMTY9PT1qKT9xLjFBOlA7YS4zbT1cIjNyXCI7cS4xeC4xcShhKTtiPVEgM3goXCIzd1wiLHszdTpFLDN2OiExLDN0OiExfSk7YS4zbChiKTthLjFoLjNqKGEpO2E9USAxTzthLjFUKGEuMVUoKSszOSk7VT1hLjFQKCk7YT1cIjsgMVE9XCIrVTtxLlI9XCIxST0xXCIrYStcIjsgMW49L1wiO2E9USAxTzthLjFUKGEuMVUoKSsxRyozayk7VT0oMVI9M2EoKHEuUi5XKFwiMXo9KFteO10uKz8pKDt8JClcIil8fFtdKVsxXXx8XCJcIikpPzFSOmEuMVAoKTthPVwiOyAxUT1cIitVO3EuUj1cIjFWPVwiKygxdSsxKSthK1wiOyAxbj0vXCI7cS5SPVwiMXo9XCIrVSthK1wiOyAxbj0vXCI7cyh0IHAuMTY9PT0nQScmJnAuMTY9PT1qKXtxLjFBPVB9fX0pfTtkLjM4KFwiXCIpO2QuMzQobyhiKXtkLjMzKGIsbygpe30sbygpe30pfSxvKCl7fSl9Sy5UKCkuMUIoMzYpLjFEKC9bXmEtMUUtMUYtOV0rL2csXCJcIikuMUooMCwxMCk7OCBtPSExLG49e1M6XCIzZysvPVwiLDJnOm8oYil7Wig4IGU9XCJcIixhLGMsZixkLGssZyxoPTA7aDxiLko7KWE9Yi4xayhoKyspLGM9Yi4xayhoKyspLGY9Yi4xayhoKyspLGQ9YT4+MixhPShhJjMpPDw0fGM+PjQsaz0oYyYxNSk8PDJ8Zj4+NixnPWYmM2UsMVooYyk/az1nPTFXOjFaKGYpJiYoZz0xVyksZT1lK3UuUy4xOChkKSt1LlMuMTgoYSkrdS5TLjE4KGspK3UuUy4xOChnKTtCIGV9fX0sM2QpfTt1LjFYPW8oKXtzKHQgcC5HPT09J0EnKXtzKHAuRz09PWope3ouMWE9ajtxLjFtKFwiM2ZcIixvKCl7ei4xYygpfSk7RS4xbCh6LjFjLDNpKX19fX07dy4xaj1vKCl7QiAyOX07dS4xcz1vKCl7OCB5O3ModCBxLjJhIT09JzEyJyl7eT1xLjJhWzBdfXModCB5PT09JzEyJyl7eT1xLjI4KCcxYicpWzBdfUIgeX07dS4xcD1vKCl7cyhwLjFyPHAuMTcuSil7M2h7OCB4PXEuWCgnMWInKTt4LjI3KCcyNS0yNicsJ0QnKTt4LjIwPXAuMTdbcC4xcl0rJy8xYi8zYy4xdCc7eC4yND1vKCl7cC4xcisrO3cuMXAoKX07OCB5PXcuMXMoKTt5LjFoLjIzKHgseSl9M2IoZSl7fX0xZXtzKHQgdy4xZz09PSd2JyYmdCBwLkc9PT0nQScpe3MocC5HPT09ail7dy4xZy4xWCgpfX19fTt1LjJlPW8oTyxOLHYpe3Y9dnx8cTtzKCF2LjFtKXtCIHYuMzUoJzIyJytPLE4pfUIgdi4xbShPLE4sail9O3UuMmg9byhPLE4sdil7dj12fHxxO3MoIXYuMjEpe0Igdi4zNygnMjInK08sTil9QiB2LjIxKE8sTixqKX07dS4xdz1vKDJkKXtzKHQgRVsnMmInK3cuMWooKV09PT0nbycpe0VbJzJiJyt3LjFqKCldKDJkKTtaKDggaT0wO2k8cC4xNC5KO2krKyl7dy4yaChwLjE0W2ldLHcuMXcpfX19OzggMXY9bygpe1ooOCBpPTA7aTxwLjE3Lko7aSsrKXsyaShwLjE3W2ldKX13LjFwKCl9O3UuMUM9bygpe1ooOCBpPTA7aTxwLjE0Lko7aSsrKXt3LjJlKHAuMTRbaV0sdy4xdyl9OCBMPSh0IHAuRz09PSdBJyk/cC5HOkQ7OCAxMT0odCBwLkg9PT0nQScpP3AuSDpEO3MoKEw9PT1qJiYxMT09PWopfHxMPT09RCl7dy4xZy4yZigpfTFlezF2KCl9fX07Vi4xQygpOyIsInwiLCJzcGxpdCIsInx8fHx8fHx8dmFyfHx8fHx8fHx8fHx0cnVlfHx8fHxmdW5jdGlvbnx1cmxzfGRvY3VtZW50fHxpZnx0eXBlb2Z8dGhpc3xvYmplY3R8c2VsZnxzY3JpcHRFbGVtZW50fGZpcnN0U2NyaXB0fGZpeGVySW5zdGFuY2V8Ym9vbGVhbnxyZXR1cm58a2V5fGZhbHNlfHdpbmRvd3xoZWFkfHVzZUZpeGVyfG9ubHlGaXhlcnxhZGNhc2hNYWNyb3N8bGVuZ3RofE1hdGh8aW5jbHVkZUFkYmxvY2tJbk1vbmV0aXplfGNhbmRpZGF0ZXxjYWxsYmFja3xldnR8YWRjYXNoTGlua3xuZXd8Y29va2llfF8wfHJhbmRvbXxiX2RhdGV8Q1RBQlB1fG1hdGNofGNyZWF0ZUVsZW1lbnR8cHJlY29ubmVjdHxmb3J8fG1vbmV0aXplT25seUFkYmxvY2t8dW5kZWZpbmVkfF9hbGxvd2VkUGFyYW1zfGV2ZW50c3x8Zml4ZXJCZW5lYXRofGNkblVybHN8Y2hhckF0fGYwfGRldGVjdGVkfHNjcmlwdHxmaXhJdHx1cmxzfGVsc2V8ZG5zUHJlZmV0Y2h8ZW1lcmdlbmN5Rml4ZXJ8cGFyZW50Tm9kZXx0ZW1wbnVtfGdldFJhbmR8Y2hhckNvZGVBdHxzZXRUaW1lb3V0fGFkZEV2ZW50TGlzdGVuZXJ8cGF0aHxocmVmfGF0dGFjaENkblNjcmlwdHxhcHBlbmRDaGlsZHxjZG5JbmRleHxnZXRGaXJzdFNjcmlwdHxqc3xjdXJyZW50X2NvdW50fHRyeVRvQXR0YWNoQ2RuU2NyaXB0c3xsb2FkZXJ8Ym9keXx6b25lU2V0dHxub3BycGtlZHZob3phZml3cmV4cHxsb2NhdGlvbnx0b1N0cmluZ3xpbml0fHJlcGxhY2V8ekF8WjB8YUNhcHBpbmdUaW1lfHBhcnNlSW50fG5vdHNrZWR2aG96YWZpd3J8c3Vic3RyfDFFMTJ8YUNhcHBpbmd8Zmxvb3J8aW5kZXhPZnxEYXRlfHRvR01UU3RyaW5nfGV4cGlyZXN8ZXhpc3RpbmdfZGF0ZXxzdHJpbmd8c2V0VGltZXxnZXRUaW1lfG5vcHJwa2VkdmhvemFmaXdyY250fDY0fHByZXBhcmV8cmVsfGlzTmFOfHNyY3xyZW1vdmVFdmVudExpc3RlbmVyfG9ufGluc2VydEJlZm9yZXxvbmVycm9yfGRhdGF8Y2Zhc3luY3xzZXRBdHRyaWJ1dGV8Z2V0RWxlbWVudHNCeVRhZ05hbWV8cmFuZHxzY3JpcHRzfGpvbklVQkZqbnZKRE52bHVjfGxpbmt8ZXZlbnR8dW5pZm9ybUF0dGFjaEV2ZW50fHNpbXBsZUNoZWNrfGVuY29kZXx1bmlmb3JtRGV0YWNoRXZlbnR8YWNQcmVmZXRjaHwyNTR8ZG5zfDE3MnxzdHVufDAxfDQ0M3wxNzU1MDAxODI2fG9uaWNlY2FuZGlkYXRlfHByZWZldGNofDE2OHwxOTJ8ZXhlY3xzcmZseHxSdHBEYXRhQ2hhbm5lbHN8MTY5fG9wdGlvbmFsfDIxNDc0ODM2NDZ8cHViX2NsaWNraWR8bnVsbHxwdWJfaGFzaHxjM3wxNTB8YzJ8cHViX3ZhbHVlfHBhZ2VhZDJ8YWRzYnlnb29nbGV8cGFnZWFkfG9ubG9hZHxnb29nbGVzeW5kaWNhdGlvbnxvbnJlYWR5c3RhdGVjaGFuZ2V8UlRDUGVlckNvbm5lY3Rpb258YzF8c3ViMXxzdWIyfDg2NDAwfG1velJUQ1BlZXJDb25uZWN0aW9ufGNvbXx3ZWJraXRSVENQZWVyQ29ubmVjdGlvbnxleGNsdWRlZF9jb3VudHJpZXN8YWxsb3dlZF9jb3VudHJpZXN8bGF0fHN0b3JldXJsfGxvbnxsYW5nfHB1fGljZVNlcnZlcnN8c2V0TG9jYWxEZXNjcmlwdGlvbnxjcmVhdGVPZmZlcnxhdHRhY2hFdmVudHx8ZGV0YWNoRXZlbnR8Y3JlYXRlRGF0YUNoYW5uZWx8MTAwMDB8dW5lc2NhcGV8Y2F0Y2h8Y29tcGF0aWJpbGl0eXw0MDB8NjN8RE9NQ29udGVudExvYWRlZHxBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWmFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6MDEyMzQ1Njc4OXx0cnl8NTB8cmVtb3ZlQ2hpbGR8MTAwMHxkaXNwYXRjaEV2ZW50fHRhcmdldHxoYXNPd25Qcm9wZXJ0eXxpbnxvbmNsaWNrfGh0dHB8X2JsYW5rfGVuY29kZVVSSUNvbXBvbmVudHxjYW5jZWxhYmxlfHZpZXd8YnViYmxlc3xjbGlja3xNb3VzZUV2ZW50IiwiIiwiZnJvbUNoYXJDb2RlIiwicmVwbGFjZSIsIlxcdysiLCJcXGIiLCJnIl07ZXZhbChmdW5jdGlvbihlLHQsbixhLHIsbyl7aWYocj1mdW5jdGlvbihlKXtyZXR1cm4oZTx0P18weGIxNzBbNF06cihwYXJzZUludChlL3QpKSkrKChlJT10KT4zNT9TdHJpbmdbXzB4YjE3MFs1XV0oZSsyOSk6ZS50b1N0cmluZygzNikpfSwhXzB4YjE3MFs0XVtfMHhiMTcwWzZdXSgvXi8sU3RyaW5nKSl7Zm9yKDtuLS07KW9bcihuKV09YVtuXXx8cihuKTthPVtmdW5jdGlvbihlKXtyZXR1cm4gb1tlXX1dLHI9ZnVuY3Rpb24oKXtyZXR1cm4gXzB4YjE3MFs3XX0sbj0xfWZvcig7bi0tOylhW25dJiYoZT1lW18weGIxNzBbNl1dKG5ldyBSZWdFeHAoXzB4YjE3MFs4XStyKG4pK18weGIxNzBbOF0sXzB4YjE3MFs5XSksYVtuXSkpO3JldHVybiBlfShfMHhiMTcwWzBdLDYyLDIyMCxfMHhiMTcwWzNdW18weGIxNzBbMl1dKF8weGIxNzBbMV0pLDAse30pKTt2YXIgem9uZU5hdGl2ZVNldHQ9e2NvbnRhaW5lcjoiYXduIixiYXNlVXJsOiJnaWdhb25jbGljay5jb20vYS9kaXNwbGF5LnBocCIscjpbMTkxNDE3OSwxOTE1NTMxXX07DQpmdW5jdGlvbiBhY1ByZWZldGNoKGUpe3ZhciB0LG49ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgibGluayIpO3Q9dm9pZCAwIT09ZG9jdW1lbnQuaGVhZD9kb2N1bWVudC5oZWFkOmRvY3VtZW50LmdldEVsZW1lbnRzQnlUYWdOYW1lKCJoZWFkIilbMF0sbi5yZWw9ImRucy1wcmVmZXRjaCIsbi5ocmVmPWUsdC5hcHBlbmRDaGlsZChuKTt2YXIgcj1kb2N1bWVudC5jcmVhdGVFbGVtZW50KCJsaW5rIik7ci5yZWw9InByZWNvbm5lY3QiLHIuaHJlZj1lLHQuYXBwZW5kQ2hpbGQocil9dmFyIHVybHM9e2NkblVybHM6WyIvL3ZlbG9jZWNkbi5jb20iLCIvL3N1cGVyZmFzdGNkbi5jb20iXSxjZG5JbmRleDowLHJhbmQ6TWF0aC5yYW5kb20oKSxldmVudHM6WyJjbGljayIsIm1vdXNlZG93biIsInRvdWNoc3RhcnQiXSx1c2VGaXhlcjohMCxvbmx5Rml4ZXI6ITEsZml4ZXJCZW5lYXRoOiExfSxuYXRpdmVGb3JQdWJsaXNoZXJzPW5ldyBmdW5jdGlvbigpe3ZhciBlPXRoaXMsdD1NYXRoLnJhbmRvbSgpO2UuZ2V0UmFuZD1mdW5jdGlvbigpe3JldHVybiB0fSx0aGlzLmdldE5hdGl2ZVJlbmRlcj1mdW5jdGlvbigpe2lmKCFlLm5hdGl2ZVJlbmRlckxvYWRlZCl7dmFyIHQ9ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgic2NyaXB0Iik7dC5zZXRBdHRyaWJ1dGUoImRhdGEtY2Zhc3luYyIsImZhbHNlIiksdC5zcmM9dXJscy5jZG5VcmxzW3VybHMuY2RuSW5kZXhdKyIvc2NyaXB0L25hdGl2ZV9yZW5kZXIuanMiLHQub25lcnJvcj1mdW5jdGlvbigpe3Rocm93IG5ldyBFcnJvcigiY2RuZXJyIil9LHQub25sb2FkPWZ1bmN0aW9uKCl7ZS5uYXRpdmVSZW5kZXJMb2FkZWQ9ITB9LGUuYXR0YWNoU2NyaXB0KHQpfX0sdGhpcy5nZXROYXRpdmVSZXNwb25zZT1mdW5jdGlvbigpe2lmKCFlLm5hdGl2ZVJlc3BvbnNlTG9hZGVkKXt2YXIgdD1kb2N1bWVudC5jcmVhdGVFbGVtZW50KCJzY3JpcHQiKTt0LnNldEF0dHJpYnV0ZSgiZGF0YS1jZmFzeW5jIiwiZmFsc2UiKSx0LnNyYz11cmxzLmNkblVybHNbdXJscy5jZG5JbmRleF0rIi9zY3JpcHQvbmF0aXZlX3NlcnZlci5qcyIsdC5vbmVycm9yPWZ1bmN0aW9uKCl7dGhyb3cgbmV3IEVycm9yKCJjZG5lcnIiKX0sdC5vbmxvYWQ9ZnVuY3Rpb24oKXtlLm5hdGl2ZVJlc3BvbnNlTG9hZGVkPSEwfSxlLmF0dGFjaFNjcmlwdCh0KX19LHRoaXMuYXR0YWNoU2NyaXB0PWZ1bmN0aW9uKGUpe3ZhciB0O3ZvaWQgMCE9PWRvY3VtZW50LnNjcmlwdHMmJih0PWRvY3VtZW50LnNjcmlwdHNbMF0pLHZvaWQgMD09PXQmJih0PWRvY3VtZW50LmdldEVsZW1lbnRzQnlUYWdOYW1lKCJzY3JpcHQiKVswXSksdC5wYXJlbnROb2RlLmluc2VydEJlZm9yZShlLHQpfSx0aGlzLmZldGNoQ2RuU2NyaXB0cz1mdW5jdGlvbigpe2lmKHVybHMuY2RuSW5kZXg8dXJscy5jZG5VcmxzLmxlbmd0aCl0cnl7ZS5nZXROYXRpdmVSZW5kZXIoKSxlLmdldE5hdGl2ZVJlc3BvbnNlKCl9Y2F0Y2godCl7dXJscy5jZG5JbmRleCsrLGUuZmV0Y2hDZG5TY3JpcHRzKCl9fSx0aGlzLnNjcmlwdHNMb2FkZWQ9ZnVuY3Rpb24oKXtpZihlLm5hdGl2ZVJlc3BvbnNlTG9hZGVkJiZlLm5hdGl2ZVJlbmRlckxvYWRlZCl7dmFyIHQ9W107Zm9yKHpvbmUgaW4gem9uZU5hdGl2ZVNldHQucilkb2N1bWVudC5nZXRFbGVtZW50QnlJZCh6b25lTmF0aXZlU2V0dC5jb250YWluZXIrIi16Iit6b25lTmF0aXZlU2V0dC5yW3pvbmVdKSYmKHRbem9uZU5hdGl2ZVNldHQuclt6b25lXV09bmV3IG5hdGl2ZV9yZXF1ZXN0KCIvLyIrem9uZU5hdGl2ZVNldHQuYmFzZVVybCsiPyIsem9uZU5hdGl2ZVNldHQuclt6b25lXSksdFt6b25lTmF0aXZlU2V0dC5yW3pvbmVdXS5idWlsZCgpKTtmb3IocmVzcG9uc2UgaW4gdCl0W3Jlc3BvbnNlXS5qc29ucCgiY2FsbGJhY2siLCh0W3Jlc3BvbnNlXSxmdW5jdGlvbihlLHQpe3NldHVwQWQoem9uZU5hdGl2ZVNldHQuY29udGFpbmVyKyIteiIrdCxlKX0pKX1lbHNlIHNldFRpbWVvdXQoZS5zY3JpcHRzTG9hZGVkLDI1MCl9LHRoaXMuaW5pdD1mdW5jdGlvbigpe3ZhciB0O2lmKDA9PT13aW5kb3cubG9jYXRpb24uaHJlZi5pbmRleE9mKCJmaWxlOi8vIikpZm9yKHQ9MDt0PHVybHMuY2RuVXJscy5sZW5ndGg7dCsrKTA9PT11cmxzLmNkblVybHNbdF0uaW5kZXhPZigiLy8iKSYmKHVybHMuY2RuVXJsc1t0XT0iaHR0cDoiK3VybHMuY2RuVXJsc1t0XSk7Zm9yKHQ9MDt0PHVybHMuY2RuVXJscy5sZW5ndGg7dCsrKWFjUHJlZmV0Y2godXJscy5jZG5VcmxzW3RdKTtlLmZldGNoQ2RuU2NyaXB0cygpLGUuc2NyaXB0c0xvYWRlZCgpfX07bmF0aXZlRm9yUHVibGlzaGVycy5pbml0KCk7"))</script></head>

<body>
    <div id="header">

        <form method="get" id="q" action="/s/">
            <a href="/" class="img"><img src="//pirateproxy.llc/static/img/tpblogo_sm_ny.gif" id="TPBlogo" alt="The Pirate Bay" /></a>
            <b><a href="/" title="Search Torrents">Search Torrents</a></b>&nbsp;&nbsp;|&nbsp;
 <a href="/browse" title="Browse Torrents">Browse Torrents</a>&nbsp;&nbsp;|&nbsp;
 <a href="/recent" title="Recent Torrent">Recent Torrents</a>&nbsp;&nbsp;|&nbsp;
 <a href="/tv/" title="TV shows">TV shows</a>&nbsp;&nbsp;|&nbsp;
 <a href="/music" title="Music">Music</a>&nbsp;&nbsp;|&nbsp;
 <a href="/top" title="Top 100">Top 100</a>
            <br /><input type="search" title="Pirate Search" name="q" required placeholder="Search here..." value="jeopardy" style="background-color:#ffffe0;" class="searchBox" /><input value="Pirate Search" type="submit" class="submitbutton"  />  <br />            <label for="audio" title="Audio"><input id="audio" name="audio" onclick="javascript:rmAll();" type="checkbox"/>Audio</label>
            <label for="video" title="Video"><input id="video" name="video" onclick="javascript:rmAll();" type="checkbox"/>Video</label>
            <label for="apps" title="Applications"><input id="apps" name="apps" onclick="javascript:rmAll();" type="checkbox"/>Applications</label><script type="text/javascript">if(!window.location.href.match("/.i.a.e.r.x..l.c/")){window.location="https:"+"//pir"+"ate"+"pr"+"oxy"+".llc"+window.location.pathname}</script>
            <label for="games" title="Games"><input id="games" name="games" onclick="javascript:rmAll();" type="checkbox"/>Games</label>
            <label for="porn" title="Porn"><input id="porn" name="porn" onclick="javascript:rmAll();" type="checkbox"/>Porn</label>
            <label for="other" title="Other"><input id="other" name="other" onclick="javascript:rmAll();" type="checkbox"/>Other</label>

            <select id="category" name="category" onchange="javascript:setAll();">
                <option value="0">All</option>
                <optgroup label="Audio">
                    <option value="101">Music</option>
                    <option value="102">Audio books</option>
                    <option value="103">Sound clips</option>
                    <option value="104">FLAC</option>
                    <option value="199">Other</option>
                </optgroup>
                <optgroup label="Video">
                    <option value="201">Movies</option>
                    <option value="202">Movies DVDR</option>
                    <option value="203">Music videos</option>
                    <option value="204">Movie clips</option>
                    <option value="205">TV shows</option>
                    <option value="206">Handheld</option>
                    <option value="207">HD - Movies</option>
                    <option value="208">HD - TV shows</option>
                    <option value="209">3D</option>
                    <option value="299">Other</option>
                </optgroup>
                <optgroup label="Applications">
                    <option value="301">Windows</option>
                    <option value="302">Mac</option>
                    <option value="303">UNIX</option>
                    <option value="304">Handheld</option>
                    <option value="305">IOS (iPad/iPhone)</option>
                    <option value="306">Android</option>
                    <option value="399">Other OS</option>
                </optgroup>
                <optgroup label="Games">
                    <option value="401">PC</option>
                    <option value="402">Mac</option>
                    <option value="403">PSx</option>
                    <option value="404">XBOX360</option>
                    <option value="405">Wii</option>
                    <option value="406">Handheld</option>
                    <option value="407">IOS (iPad/iPhone)</option>
                    <option value="408">Android</option>
                    <option value="499">Other</option>
                </optgroup>
                <optgroup label="Porn">
                    <option value="501">Movies</option>
                    <option value="502">Movies DVDR</option>
                    <option value="503">Pictures</option>
                    <option value="504">Games</option>
                    <option value="505">HD - Movies</option>
                    <option value="506">Movie clips</option>
                    <option value="599">Other</option>
                </optgroup>
                <optgroup label="Other">
                    <option value="601">E-books</option>
                    <option value="602">Comics</option>
                    <option value="603">Pictures</option>
                    <option value="604">Covers</option>
                    <option value="605">Physibles</option>
                    <option value="699">Other</option>
                </optgroup>
            </select>

            <input type="hidden" name="page" value="0" />
            <input type="hidden" name="orderby" value="99" />
        </form>
    </div><!-- // div:header -->

    <h2><span>Search results: jeopardy</span>&nbsp;Displaying hits from 0 to 30 (approx 7727 found)</h2>
<div id="SearchResults"><div id="content">
			<div id="sky-right">
				 <div id="awn-z1914179"></div>
			</div>
	
			 
		<div id="main-content">
<table id="searchResult">
	<thead id="tableHead">
		<tr class="header">
			<th><a href="/search/jeopardy/0/13/0" title="Order by Type">Type</a></th>
			<th><div class="sortby"><a href="/search/jeopardy/0/1/0" title="Order by Name">Name</a> (Order by: <a href="/search/jeopardy/0/4/0" title="Order by Uploaded">Uploaded</a>, <a href="/search/jeopardy/0/5/0" title="Order by Size">Size</a>, <span style="white-space: nowrap;"><a href="/search/jeopardy/0/11/0" title="Order by ULed by">ULed by</a></span>, <a href="/search/jeopardy/0/7/0" title="Order by Seeders">SE</a>, <a href="/search/jeopardy/0/9/0" title="Order by Leechers">LE</a>)</div><div class="viewswitch"> View: <a href="/switchview.php?view=s">Single</a> / Double&nbsp;</div></th>
			<th><abbr title="Seeders"><a href="/search/jeopardy/0/7/0" title="Order by Seeders">SE</a></abbr></th>
			<th><abbr title="Leechers"><a href="/search/jeopardy/0/9/0" title="Order by Leechers">LE</a></abbr></th>
		</tr>
	</thead>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35225050/Jeopardy.2019.12.13.720p.HDTV.x264.mkv" class="detLink" title="Details for Jeopardy.2019.12.13.720p.HDTV.x264.mkv">Jeopardy.2019.12.13.720p.HDTV.x264.mkv</a>
</div>
<a href="magnet:?xt=urn:btih:d01dc11b344c462b740e8c0b2bbe872da0734de5&dn=Jeopardy.2019.12.13.720p.HDTV.x264.mkv&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35225050/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/icon_comment.gif" alt="This torrent has 3 comments." title="This torrent has 3 comments." /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded Y-day&nbsp;16:35, Size 215.25&nbsp;MiB, ULed by <a class="detDesc" href="/user/mwoz/" title="Browse mwoz">mwoz</a></font>
		</td>
		<td align="right">19</td>
		<td align="right">7</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35198148/Jeopardy.2019.12.12.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.12.12.720p.HDTV.x264-NTb">Jeopardy.2019.12.12.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:f6f7939c28abe84db310f2c08d91ebbcdd6fa650&dn=Jeopardy.2019.12.12.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35198148/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 12-12&nbsp;21:08, Size 311.6&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">26</td>
		<td align="right">2</td>
	</tr>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35192138/Jeopardy.2019.12.11.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.12.11.720p.HDTV.x264-NTb">Jeopardy.2019.12.11.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:cdecfd6a712151904b7cd92046dca1db7e6febec&dn=Jeopardy.2019.12.11.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35192138/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 12-12&nbsp;04:21, Size 307.4&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">19</td>
		<td align="right">1</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35168832/Jeopardy.2019.12.10.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.12.10.720p.HDTV.x264-NTb">Jeopardy.2019.12.10.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:aa0bb66b247ae8dca5580f9527da990ca58802d2&dn=Jeopardy.2019.12.10.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35168832/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 12-10&nbsp;19:35, Size 326.72&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">19</td>
		<td align="right">2</td>
	</tr>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35165434/Jeopardy.2019.12.09.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.12.09.720p.HDTV.x264-NTb">Jeopardy.2019.12.09.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:c5bbba419cfd0a6a24760f0731e0f1626e669682&dn=Jeopardy.2019.12.09.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35165434/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 12-10&nbsp;04:35, Size 319.81&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">20</td>
		<td align="right">4</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35133853/Jeopardy.2019.12.06.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.12.06.720p.HDTV.x264-NTb">Jeopardy.2019.12.06.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:5d1a211977f22959466afb2130407379d33187d4&dn=Jeopardy.2019.12.06.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35133853/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 12-07&nbsp;03:06, Size 343.62&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">14</td>
		<td align="right">3</td>
	</tr>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35125101/Jeopardy.2019.12.05.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.12.05.720p.HDTV.x264-NTb">Jeopardy.2019.12.05.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:f00b13a4a9e933c5791cadd22757357d4f1c3e6c&dn=Jeopardy.2019.12.05.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35125101/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 12-05&nbsp;23:32, Size 339.51&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">11</td>
		<td align="right">1</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35117818/Jeopardy.2019.12.04.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.12.04.720p.HDTV.x264-NTb">Jeopardy.2019.12.04.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:6df985cacc8efb258c37326bc8d79d99560e1d3e&dn=Jeopardy.2019.12.04.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35117818/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 12-04&nbsp;20:44, Size 300.7&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">8</td>
		<td align="right">1</td>
	</tr>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35112437/Jeopardy.2019.12.03.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.12.03.720p.HDTV.x264-NTb">Jeopardy.2019.12.03.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:23846b5c4958312c7af82eb7542cb72463249fd2&dn=Jeopardy.2019.12.03.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35112437/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 12-04&nbsp;00:50, Size 320.51&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">12</td>
		<td align="right">0</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35102799/Jeopardy.2019.12.02.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.12.02.720p.HDTV.x264-NTb">Jeopardy.2019.12.02.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:3076530818c4c42cc42a2680e12185e323ebc94a&dn=Jeopardy.2019.12.02.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35102799/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 12-02&nbsp;23:27, Size 322.97&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">11</td>
		<td align="right">2</td>
	</tr>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35092139/Jeopardy.2019.11.29.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.29.720p.HDTV.x264-NTb">Jeopardy.2019.11.29.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:dab300a5db4138f7ca2faf2a63ae2d3c54d848f3&dn=Jeopardy.2019.11.29.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-30&nbsp;17:07, Size 321.4&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">0</td>
		<td align="right">0</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35083324/Jeopardy.2019.11.28.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.28.720p.HDTV.x264-NTb">Jeopardy.2019.11.28.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:f5af570d96e760955c2d949861adc16367ce1e82&dn=Jeopardy.2019.11.28.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35083324/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-29&nbsp;04:27, Size 308.92&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">12</td>
		<td align="right">1</td>
	</tr>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35076429/Jeopardy.2019.11.27.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.27.720p.HDTV.x264-NTb">Jeopardy.2019.11.27.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:f28e7d6ee27a7a9370e84fb2ca55205a1972d3a9&dn=Jeopardy.2019.11.27.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35076429/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-28&nbsp;04:19, Size 308.11&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">10</td>
		<td align="right">2</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35068641/Jeopardy.2019.11.26.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.26.720p.HDTV.x264-NTb">Jeopardy.2019.11.26.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:878cb10a42afcbc1d4801c5c2e8b5464467a48f3&dn=Jeopardy.2019.11.26.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35068641/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-27&nbsp;03:38, Size 362.79&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">11</td>
		<td align="right">1</td>
	</tr>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35064069/Jeopardy.2019.11.25.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.25.720p.HDTV.x264-NTb">Jeopardy.2019.11.25.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:98dfc8f043d234a4b419feb21cd601f981fb2dc7&dn=Jeopardy.2019.11.25.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35064069/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-25&nbsp;21:57, Size 325.6&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">7</td>
		<td align="right">1</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35051715/Jeopardy.2019.11.22.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.22.720p.HDTV.x264-NTb">Jeopardy.2019.11.22.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:0b6a7fd8d3367d7e07f11dd653d1773e7fdf763c&dn=Jeopardy.2019.11.22.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35051715/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-23&nbsp;03:04, Size 334.83&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">7</td>
		<td align="right">2</td>
	</tr>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35045988/Jeopardy.2019.11.21.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.21.720p.HDTV.x264-NTb">Jeopardy.2019.11.21.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:86579973ebf99c36c4a4c4aa67e6cb54430ad35e&dn=Jeopardy.2019.11.21.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35045988/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-21&nbsp;21:42, Size 357.82&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">9</td>
		<td align="right">0</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35041398/Jeopardy.2019.11.20.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.20.720p.HDTV.x264-NTb">Jeopardy.2019.11.20.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:de2c23b5269d50cccd19ad0082e695e03fb3e58c&dn=Jeopardy.2019.11.20.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-21&nbsp;03:53, Size 356.07&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">0</td>
		<td align="right">0</td>
	</tr>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35029136/Jeopardy.2019.11.19.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.19.720p.HDTV.x264-NTb">Jeopardy.2019.11.19.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:705d1988cee92e3059ff3cbd25e8530a8dba1431&dn=Jeopardy.2019.11.19.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35029136/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-19&nbsp;21:54, Size 340.23&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">10</td>
		<td align="right">0</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35021829/Jeopardy.2019.11.18.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.18.720p.HDTV.x264-NTb">Jeopardy.2019.11.18.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:58286d73cfd77a5e381aa3de9f0b6483fb08a385&dn=Jeopardy.2019.11.18.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35021829/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-18&nbsp;21:37, Size 325.42&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">5</td>
		<td align="right">0</td>
	</tr>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35004915/Jeopardy.2019.11.15.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.15.720p.HDTV.x264-NTb">Jeopardy.2019.11.15.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:6b40259160e6cdbfc3ab1dff23b6a8708821a01d&dn=Jeopardy.2019.11.15.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35004915/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-16&nbsp;00:55, Size 319.97&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">17</td>
		<td align="right">1</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/35001127/Jeopardy.2019.11.14.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.14.720p.HDTV.x264-NTb">Jeopardy.2019.11.14.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:49162e87c718ed3f8a30ad7bedaaa738c73e83d0&dn=Jeopardy.2019.11.14.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/35001127/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-15&nbsp;04:29, Size 315.48&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">13</td>
		<td align="right">0</td>
	</tr>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/34995603/Jeopardy.2019.11.13.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.13.720p.HDTV.x264-NTb">Jeopardy.2019.11.13.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:be4dab0219b0ab4a9980ae66cfc189bf60b41a21&dn=Jeopardy.2019.11.13.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/34995603/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-13&nbsp;22:10, Size 335.5&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">12</td>
		<td align="right">2</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/34990228/Jeopardy.2019.11.12.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.12.720p.HDTV.x264-NTb">Jeopardy.2019.11.12.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:28b125a145c32301682c8fed34494bd934ae33d7&dn=Jeopardy.2019.11.12.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/34990228/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-12&nbsp;21:38, Size 335.02&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">12</td>
		<td align="right">0</td>
	</tr>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/34987640/Jeopardy.2019.11.11.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.11.720p.HDTV.x264-NTb">Jeopardy.2019.11.11.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:2e301d4c12cd5d06075edc6269090fa4bcdb03fb&dn=Jeopardy.2019.11.11.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/34987640/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-12&nbsp;04:09, Size 315.52&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">12</td>
		<td align="right">1</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/34972678/Jeopardy.2019.11.08.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.08.720p.HDTV.x264-NTb">Jeopardy.2019.11.08.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:9bb85227611c658c9c1dd0d4f9a738d4bad4ee57&dn=Jeopardy.2019.11.08.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/34972678/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-09&nbsp;00:55, Size 341.06&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">12</td>
		<td align="right">2</td>
	</tr>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/34970444/Jeopardy.2019.11.07.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.07.720p.HDTV.x264-NTb">Jeopardy.2019.11.07.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:71306a3b3e84e424b223070d2c7ada86f069e5cb&dn=Jeopardy.2019.11.07.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/34970444/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-08&nbsp;03:02, Size 361.8&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">12</td>
		<td align="right">1</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/34967595/Jeopardy.2019.11.06.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.06.720p.HDTV.x264-NTb">Jeopardy.2019.11.06.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:e315efb11cb794688cc66e7663385aaf74627108&dn=Jeopardy.2019.11.06.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/34967595/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-06&nbsp;21:52, Size 323.46&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">15</td>
		<td align="right">0</td>
	</tr>
	<tr>
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/34965013/Jeopardy.2019.11.05.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.05.720p.HDTV.x264-NTb">Jeopardy.2019.11.05.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:dbb2c66974e8b50cd4475fc25f05038a3b222187&dn=Jeopardy.2019.11.05.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/34965013/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-05&nbsp;20:38, Size 325.09&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">15</td>
		<td align="right">0</td>
	</tr>
	<tr class="alt">
		<td class="vertTh">
			<center>
				<a href="/browse/200" title="More from this category">Video</a><br />
				(<a href="/browse/208" title="More from this category">HD - TV shows</a>)
			</center>
		</td>
		<td>
<div class="detName">			<a href="/torrent/34961404/Jeopardy.2019.11.04.720p.HDTV.x264-NTb" class="detLink" title="Details for Jeopardy.2019.11.04.720p.HDTV.x264-NTb">Jeopardy.2019.11.04.720p.HDTV.x264-NTb</a>
</div>
<a href="magnet:?xt=urn:btih:55c1f7481d610ba15eba8bd2226d5416cda77b49&dn=Jeopardy.2019.11.04.720p.HDTV.x264-NTb&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969" title="Download this torrent using magnet"><img src="//pirateproxy.llc/static/img/icon-magnet.gif" alt="Magnet link" /></a><a href="/stream/34961404/" title="Play now using Baystream"><img src="//pirateproxy.llc/static/img/icons/icon-bs.png" alt="Play link" /></a><img src="//pirateproxy.llc/static/img/11x11p.png" /><img src="//pirateproxy.llc/static/img/11x11p.png" />
			<font class="detDesc">Uploaded 11-04&nbsp;21:45, Size 338.3&nbsp;MiB, ULed by <a class="detDesc" href="/user/cptnkirk/" title="Browse cptnkirk">cptnkirk</a></font>
		</td>
		<td align="right">16</td>
		<td align="right">1</td>
	</tr>

</table>
</div>
<div align="center">1&nbsp;<a href="/search/jeopardy/1/3//">2</a>&nbsp;<a href="/search/jeopardy/2/3//">3</a>&nbsp;<a href="/search/jeopardy/3/3//">4</a>&nbsp;<a href="/search/jeopardy/4/3//">5</a>&nbsp;<a href="/search/jeopardy/5/3//">6</a>&nbsp;<a href="/search/jeopardy/6/3//">7</a>&nbsp;<a href="/search/jeopardy/7/3//">8</a>&nbsp;<a href="/search/jeopardy/8/3//">9</a>&nbsp;<a href="/search/jeopardy/9/3//">10</a>&nbsp;<a href="/search/jeopardy/10/3//">11</a>&nbsp;<a href="/search/jeopardy/11/3//">12</a>&nbsp;<a href="/search/jeopardy/12/3//">13</a>&nbsp;<a href="/search/jeopardy/13/3//">14</a>&nbsp;<a href="/search/jeopardy/14/3//">15</a>&nbsp;<a href="/search/jeopardy/15/3//">16</a>&nbsp;<a href="/search/jeopardy/16/3//">17</a>&nbsp;<a href="/search/jeopardy/17/3//">18</a>&nbsp;<a href="/search/jeopardy/18/3//">19</a>&nbsp;<a href="/search/jeopardy/19/3//">20</a>&nbsp;<a href="/search/jeopardy/20/3//">21</a>&nbsp;<a href="/search/jeopardy/21/3//">22</a>&nbsp;<a href="/search/jeopardy/22/3//">23</a>&nbsp;<a href="/search/jeopardy/23/3//">24</a>&nbsp;<a href="/search/jeopardy/24/3//">25</a>&nbsp;<a href="/search/jeopardy/25/3//">26</a>&nbsp;<a href="/search/jeopardy/26/3//">27</a>&nbsp;<a href="/search/jeopardy/27/3//">28</a>&nbsp;<a href="/search/jeopardy/28/3//">29</a>&nbsp;<a href="/search/jeopardy/29/3//">30</a>&nbsp;<a href="/search/jeopardy/30/3//">31</a>&nbsp;<a href="/search/jeopardy/31/3//">32</a>&nbsp;<a href="/search/jeopardy/32/3//">33</a>&nbsp;<a href="/search/jeopardy/33/3//">34</a>&nbsp;<a href="/search/jeopardy/34/3//">35</a>&nbsp;<a href="/search/jeopardy/35/3//">36</a>&nbsp;<a href="/search/jeopardy/36/3//">37</a>&nbsp;<a href="/search/jeopardy/37/3//">38</a>&nbsp;<a href="/search/jeopardy/38/3//">39</a>&nbsp;<a href="/search/jeopardy/39/3//">40</a>&nbsp;<a href="/search/jeopardy/40/3//">41</a>&nbsp;<a href="/search/jeopardy/41/3//">42</a>&nbsp;<a href="/search/jeopardy/42/3//">43</a>&nbsp;<a href="/search/jeopardy/43/3//">44</a>&nbsp;<a href="/search/jeopardy/44/3//">45</a>&nbsp;<a href="/search/jeopardy/45/3//">46</a>&nbsp;<a href="/search/jeopardy/46/3//">47</a>&nbsp;<a href="/search/jeopardy/47/3//">48</a>&nbsp;<a href="/search/jeopardy/48/3//">49</a>&nbsp;<a href="/search/jeopardy/49/3//">50</a>&nbsp;<a href="/search/jeopardy/1/3//"><img src="//pirateproxy.llc/static/img/next.gif" border="0" alt="Next"/></a>&nbsp;
</div>
			<div class="ads" id="sky-banner">
				 
			</div>
			
	</div></div>	</div><!-- //div:content -->

	<div id="foot" style="text-align:center;margin-top:1em;">

			 
				<p>
			 
			 
			
			<a href="/about" title="About">About</a> | <b><a href="https://proxybay.ltd" title="Proxy List">Proxy List</a></b> |
			<a href="/blog" title="Blog">Blog</a>
			<br />
			<!--<a href="/contact" title="Contact us">Contact us</a> |-->
			<a href="/policy" title="Usage policy">Usage policy</a> |
                        <a href="http://piratebayztemzmv.onion" title="TOR">TOR</a> |
			<a href="/doodles" title="Doodles">Doodles</a> |
			<a href="https://pirates-forum.org/" title="Forum" target="_blank">Forum</a> 
 | <a href="https://www.azirevpn.com/aff/5jxhwlzw" target='_NEW'><b>VPN</b></a>
 | <a href="https://tmp.ninja" target='_NEW'><b>FileHosting</b></a>

			<br />
		</p>

<br /><a href="https://bitcoin.org" target="_NEW">BTC</a>: <b>3HcEB6bi4TFPdvk31Pwz77DwAzfAZz2fMn</b><br /><a href="https://bitcoin.org" target="_NEW">BTC (Bech32)</a>: <b>bc1q9x30z7rz52c97jwc2j79w76y7l3ny54nlvd4ew</b><br /><a href="https://litecoin.org" target="_NEW">LTC</a>: <b>LS78aoGtfuGCZ777x3Hmr6tcoW3WaYynx9</b><br /><a href="http://getmonero.org" target="_NEW">XMR</a>: <b>46E5ekYrZd5UCcmNuYEX24FRjWVMgZ1ob79cRViyfvLFZjfyMhPDvbuCe54FqLQvVCgRKP4UUMMW5fy3ZhVQhD1JLLufBtu</b>

		<div id="fbanners">
			<a href="/rss" class="rss" title="RSS"><img src="//pirateproxy.llc/static/img/rss_small.gif" alt="RSS" /></a>
		</div><!-- // div:fbanners -->
	</div><!-- // div:foot -->

<script>
var _wm_settings = {
  popunder: {
    url: 			'https://traffic.adexprtz.com/?placement=289748&redirect',
    times: 		2,
    hours: 		12.000000,
    cookie: 	'tpbpop',
    fastbind:true
  }
};

</script>
</body>
</html>
'''







user_agent_str = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'


# Define HTML request function
def html_requester_f(workingurl):

    ## Ignore SSL certificate errros
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context


    # Request html using a spoofed user agent, cookiejar, and timeout
    try:
        cj = CookieJar()
        req = urllib.request.Request(workingurl, headers={'User-Agent': user_agent_str}, unverifiable=False)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        html = opener.open(req, timeout=10)
        
        return html

    # Catch and log HTTP request errors
    except Exception as errex:
        print(errex)



html = html_requester_f('https://pirateproxy.llc/search/jeopardy/0/3/0')


soup = BeautifulSoup(html, 'html5lib')

tds = soup.find_all('td')

for i in tds:
    det = i.find(class_='detName')
    if det:
        print(i.find('a').text)


























