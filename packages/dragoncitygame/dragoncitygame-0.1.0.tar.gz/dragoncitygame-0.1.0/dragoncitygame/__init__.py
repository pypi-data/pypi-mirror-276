from bs4 import BeautifulSoup, Tag
from pydantic import validate_call
from datetime import datetime
import httpx
import re

@validate_call
def get_month_abbreviation(month_number: int) -> str:
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    return months[month_number - 1]

@validate_call
def get_month_name(month_number: int) -> str:
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    return months[month_number - 1]

@validate_call
def month_name_to_number(month_name: str, language: str) -> int:
    month_name = month_name.lower()
    
    months = {
        "pt-BR": ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"],
        "en": ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"],
        "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    }
    
    return months[language].index(month_name.lower()) + 1

@validate_call
def date_to_timestamp(
    day: int,
    month: str,
    year: int,
    language: str
) -> int:
    return int(
        datetime(
            year = year,
            month = month_name_to_number(month, language),
            day = day
        ).timestamp()
    )

@validate_call(config = dict(arbitrary_types_allowed = True))
def parse_body_element(body_element: Tag, year: int, language: str) -> dict:
    summary = ""
    summary_is_finished = False
    events = []
    
    date_range_patterns = {
        "pt-BR": [
            re.compile(r"De (\d{1,2}) de (\w+) a (\d{1,2}) de (\w+)"),
            re.compile(r"De (\d{1,2}) a (\d{1,2}) de (\w+)")
        ],
        "en": [
            re.compile(r"(\d{1,2}) (\w+) - (\d{1,2}) (\w+)")
        ],
        "es": [
            re.compile(r"Del (\d{1,2}) de (\w+) al (\d{1,2}) de (\w+)"),
            re.compile(r"Del (\d{1,2}) al (\d{1,2}) de (\w+)")
        ]
    }

    webstore_gift_card = body_element.select_one(".css-1r9sjag p")
    paragraphs = body_element.select("p")
    
    for paragraph in paragraphs:
        text = paragraph.text
        
        if paragraph == webstore_gift_card or text == "" or text.startswith("AVISO LEGAL:") or text.startswith("DISCLAIMER:"):
            continue
        
        if text.startswith("De ") or text[0].isnumeric() or text.startswith("Del "):
            if len(events) > 0:
                if not "new_dragons" in events[-1]:
                    events[-1]["new_dragons"] = []
                    
                if not "collection_dragons" in events[-1]:
                    events[-1]["collection_dragons"] = []
                    
                if not "featured_dragons" in events[-1]:
                    events[-1]["featured_dragons"] = []
            
            if not summary_is_finished:
                summary_is_finished = True
            
            title = ":".join(text.split(":")[1:]).strip()
            date_range_match = None
            for pattern in date_range_patterns[language]:
                date_range_match = pattern.search(text)
                if date_range_match:
                    break
            
            if date_range_match:
                date_range_match_groups = date_range_match.groups()
                
                if len(date_range_match_groups) == 4:
                    from_day, from_month, to_day, to_month = date_range_match_groups
                    
                elif len(date_range_match_groups) == 3:
                    from_day, to_day, to_month = date_range_match_groups
                    from_month = str(to_month)
                    
                from_timestamp = date_to_timestamp(int(from_day), from_month, year, language)
                to_timestamp = date_to_timestamp(int(to_day), to_month, year, language)
                    
            current_event = {
                "title": title,
                "availability": {
                    "from": from_timestamp,
                    "to": to_timestamp
                }
            }
            
            events.append(current_event)
        
        elif text.startswith("Novo Dragão: ") or text.startswith("New Dragon: ") or text.startswith("Nuevo dragón: "):
            new_dragon = text.split(": ")[1].strip()
            
            if "new_dragons" in events[-1]:
                events[-1]["new_dragons"].append(new_dragon)
                
            else:
                events[-1]["new_dragons"] = [new_dragon]
        
        elif text.startswith("Dragão de coleção: ") or text.startswith("Collection Dragon: ") or text.startswith("Colección de dragones: "):
            collection_dragon = text.split(": ")[1].strip()
            
            if "collection_dragons" in events[-1]:
                events[-1]["collection_dragons"].append(collection_dragon)
                
            else:
                events[-1]["collection_dragons"] = [collection_dragon]
        
        elif text.startswith("Dragão em destaque: ") or text.startswith("Featured Dragon: ") or text.startswith("Dragón destacado: "):
            featured_dragon = text.split(": ")[1].strip()
            
            if "featured_dragons" in events[-1]:
                events[-1]["featured_dragons"].append(featured_dragon)
                
            else:
                events[-1]["featured_dragons"] = [featured_dragon]
            
        elif not summary_is_finished:
            summary += f"{text}\n"
            
    if not "new_dragons" in events[-1]:
        events[-1]["new_dragons"] = []
        
    if not "collection_dragons" in events[-1]:
        events[-1]["collection_dragons"] = []
        
    if not "featured_dragons" in events[-1]:
        events[-1]["featured_dragons"] = []
    
    summary = summary.strip()
    
    return {
        "summary": summary,
        "events": events
    }

class DragonCityGame:
    def __init__(self) -> None:
        pass

    @validate_call
    def get_monthly_events(
        self,
        language: str,
        month: int,
        year: int
    ) -> dict:
        if language.startswith("en"):
            language = "en"
            
        adjusted_language = language + "/" if language != "en" else ""
        
        
        try:
            month_abbreviated = get_month_abbreviation(month)
            url = f"https://www.dragoncitygame.com/{adjusted_language}news/upcoming-events-{month_abbreviated}-{year}"
            response = httpx.get(url)
            
            if response.status_code == 404:
                raise Exception("Not Found Page")
            
        except:
            complete_month = get_month_name(month)
            url = f"https://www.dragoncitygame.com/{adjusted_language}news/upcoming-events-{complete_month}-{year}"
            response = httpx.get(url)
            
        html = response.text
        
        post_date_patters = {
            "pt-BR": re.compile(r"(\d{1,2}) de (\w+) de (\d{1,4})"),
            "en": re.compile(r"(\w+) (\d{1,2}), (\d{1,4})"),
            "es": re.compile(r"(\d{1,2}) de (\w+) de (\d{1,4})")
        }

        soup = BeautifulSoup(html, "html.parser")
        
        post_date_text = soup.select_one("time").text
        post_date_match = post_date_patters[language].search(post_date_text)
        
        posted_on = None
        
        if post_date_match:
            if language == "pt-BR":
                post_day, post_month_name, post_year = post_date_match.groups()
                
            elif language == "en":
                post_month_name, post_day, post_year = post_date_match.groups()
                
            elif language == "es":
                post_day, post_month_name, post_year = post_date_match.groups()
                
            print(
                int(post_day),
                month_name_to_number(post_month_name, language),
                int(post_year)
            )
                
            posted_on = int(
                    datetime(
                    day = int(post_day),
                    month = month_name_to_number(post_month_name, language),
                    year = int(post_year)
                ).timestamp()
            )

        post_title = soup.select_one(".css-mdy10g").text
        thumbnail_image_url = soup.select_one(".css-1druz71 img").attrs["src"]
        body_element = soup.select_one(".css-1druz71")

        return {
            "url": url,
            "posted_on": posted_on,
            "title": post_title,
            "thumbnail_image_url": thumbnail_image_url,
            **parse_body_element(body_element, year, language)
        }