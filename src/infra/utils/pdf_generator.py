import markdown2
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from io import BytesIO

font_config = FontConfiguration()
css = CSS(
    string='''
        @font-face {
            font-family: 'shabnam';
            src: url('../fonts/shabnam-light.ttf');
            font-weight: 300
        }
        @font-face {
            font-family: 'shabnam';
            src: url('../fonts/shabnam.ttf');
            font-weight: 400
        }
        @font-face {
            font-family: 'shabnam';
            src: url('../fonts/shabnam-bold.ttf');
            font-weight: 700
        }
        @font-face {
            font-family: 'shabnam';
            src: url('../fonts/shabnam-bold.ttf');
            font-weight: 800
        }
        @font-face {
            font-family: 'shabnam';
            src: url('../fonts/shabnam-bold.ttf');
            font-weight: 900
        }

        * {
            font-family: 'shabnam';
            direction: rtl;
            text-align: right;
        }
    ''',
    font_config=font_config,
)

def generate_pdf(content: str, with_style: bool = True) -> BytesIO:
    
    content = markdown2.markdown(content)
    out_put: BytesIO = BytesIO()
    
    if with_style:
        HTML(
            string=content
        ).write_pdf(
            out_put,
            stylesheets=[
                css,
            ],
            font_config=font_config,
        )
        out_put.seek(0)
    else:
        HTML(
            string=content
        ).write_pdf(
            out_put,
            font_config=font_config,
        )
        out_put.seek(0)
        
    return out_put
