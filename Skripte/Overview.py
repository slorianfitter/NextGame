import streamlit as st
from functions.load_data import load_all_data


game_data, game_data_0_1, game_image_desc_data , image_and_description_data = load_all_data()

st.set_page_config(
    page_title="Projektübersicht",
)

st.header("Steamdashboard / Empfehlungssystem")



st.markdown(
    """
    ---
    Dies ist ein Multipage-Projekt, welches Steam-Userdaten nutzt und – sofern gewünscht – eine Empfehlung für ein nächstes Spiel ausgibt.

    ---

    ## 📚 Inhaltsverzeichnis
    1. [Hintergrund](#1-hintergrund)
    2. [Daten](#2-daten)
        - 2.1 [Tutorial: Wie du an deine Daten kommst](#21-tutorial-wie-du-an-deine-daten-kommst)
            - 2.1.1 [Steam-Key beantragen](#211-steam-key-beantragen)
            - 2.1.2 [Steam-ID besorgen](#212-steam-id-besorgen)
            - 2.1.3 [Profildaten abrufen](#213-profildaten-abrufen)
    3. [Filtermöglichkeiten](#3-filtermöglichkeiten)
    4. [Profilinformationen](#4-profilinformationen)
    5. [Zufällige Spielempfehlung](#5-zufällige-spielempfehlung)
    6. [Das Herz des Projekts – individuelle Spieleempfehlung](#6-das-herz-des-projekts--individuelle-spieleempfehlung)
        - 6.1. [Profil](#61-profil)
        - 6.2. [Modelle](#62-modelle)
            - 6.2.1. [Distanzmodell](#621-distanzmodell-teilweise-ungenau)
            - 6.2.2. [Distanzmodell in Kombination mit Reviews](#622-distanzmodell-in-kombination-mit-reviews)
    7. [Disclaimer](#7-disclaimer)

    ---

    ## 1. Hintergrund

    Das Projekt habe ich angefangen zu gestalten, da ich die schiere Menge an Spielen auf dem Markt inzwischen unfassbar unübersichtlich finde. Dies führt bei mir dazu, dass ich, wenn ich ein neues Spiel suche, quasi durch den Steam Store „doomscrolle“, dabei aber kein neues Spiel finde.

    Steam selbst stellt natürlich auch eigene Vorschläge bereit. Das Problem hierbei ist allerdings, dass Steam nicht nur meine Userdaten nutzt, sondern mich gleichzeitig auch mit anderen Usern vergleicht und mir darauf basierend Vorschläge macht. Es ist also eine Art: User B hat Spiel Y und X gespielt, du hast Spiel Y gespielt und es gefällt dir. Spiel X ist ähnlich, also hier der Vorschlag. Quasi ein einfaches kollaboratives Empfehlungssystem.

    Was mich daran jedoch stört, ist, dass nicht nur geschaut wird, ob es eine sinnvolle Empfehlung ist, sondern dass natürlich auch ein monetärer Anreiz existiert. Ich selbst kenne natürlich nicht die Margen bei Steam. Wenn ich allerdings in der Lage wäre, einen Algorithmus zu schreiben, den ich nicht offenlegen muss, und eine Multimilliarden-Dollar-Company wäre, dann würde ich vermutlich teure Spiele und Spiele mit hohen Margen bevorzugt vorschlagen.

    Das führt dazu, dass es Tausende gute Spiele gibt, die keine Aufmerksamkeit bekommen – oder zumindest nicht die Aufmerksamkeit, die sie verdienen.

    Mein einfacher Algorithmus ignoriert all diese monetären Aspekte und kann in der Theorie auch Hidden Gems von kleinen Entwicklerstudios empfehlen.

    ---

    ## 2. Daten

    Steam ist sehr transparent, was Daten angeht. Jeder kann sich sämtliche Spieldaten selbst beschaffen. Das Scraping von reinen Spieldaten ist nicht verboten, und Steam selbst stellt einige APIs bereit.

    Ein tolles Feature bei Steam ist, dass ich als Nutzer einen Überblick über meine Spiele und meine Spielzeit habe. Alles ist seit Jahrzehnten ordentlich dokumentiert. So kann ich selbst bei Steam einen API-Key beantragen und meine Daten exportieren.

    
    ### 2.1 Tutorial: Wie du an deine Daten kommst, um diese App nutzen zu können

    
    #### 2.1.1 Steam-Key beantragen

    Alle notwendigen Informationen befinden sich auf folgender Webseite:  
    https://steamcommunity.com/dev

    Wir klicken auf „by filling out this form“ und folgen anschließend den Anweisungen. Haben wir alle notwendigen Schritte erfüllt, bekommen wir einen Steam-Web-API-Schlüssel. Dieser ist einzigartig und sollte nicht geteilt werden.

    Dieser Schlüssel wird benötigt, um unsere Profildaten abzurufen.

    
    #### 2.1.2 Steam-ID besorgen

    Jeder Nutzer bei Steam hat eine eigene Steam-ID. Diese ist einfach herauszufinden.  
    Klicke ich auf mein Profil im Webbrowser, befinde ich mich auf folgender Seite:

    https://steamcommunity.com/profiles/76561198798886462/

    Die lange Zahl ist hierbei meine Steam-ID, also z. B. 76561198798886462.

    
    #### 2.1.3 Profildaten abrufen

    Zuerst müssen Bibliotheken installiert werden.


    
    ```{cmd}
    pip install requests
    ```
    ```{cmd}
    pip install pandas
    ```

    Sind die Bibliotheken installiert, kann nun folgender Code ausgeführt werden. Gerne hierfür Copy-Paste nutzen oder einfach die Datei aus dem Repository verwenden (Skripte/get_data/steam_user_daten.py).
    ```{python}
    import requests
    import pandas as pd
    ```
    Nun benötigen wir die zuvor besorgte Steam-ID und den Steam-Key.
    ```{python}
    key = "DEIN_KEY"
    steam_id = "DEINE_STEAM_ID"
    ```
    
    Anschließend können wir die Daten abrufen und als CSV-Datei speichern. Diese Datei kann anschließend auf der Seite „Data Upload“ hochgeladen werden.
    Beachte. Wenn schon einmal Daten hochgeladen wurden befinden sie sich im Cache. Auch wenn dann die Datei nicht mehr angezeigt wird, funktioniert noch alles wie es soll. 

    ```{python}
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={key}&steamid={steam_id}2&include_appinfo=1&include_played_free_games=1&format=json"

    res = requests.get(url).json()
    games = res["response"]["games"]

    df = pd.DataFrame(games)

    # Stunden-Spalte hinzufügen
    df["hours_played"] = (df["playtime_forever"] / 60).round(2)

    # Excel-Datei schreiben
    df.to_csv("D:/Projekte/spielvorschlag/data/eigene_steam_daten.csv", index=False)

    print("CSV-Datei erstellt: eigene_steam_daten.csv")
    
    ```
    
    ---

    ## 3. Filtermöglichkeiten

    Auf Seite 3 der App („Filter Optionen“) können wir, wenn wir möchten, bestimmte Informationen unseres Profils filtern. Der Filter hat jedoch nur Einfluss auf Seite 4 („Profil- und Spieleinformationen“).

    Wenn Filter ausgewählt sind, muss hierfür lediglich einmal auf „Filter anwenden“ geklickt werden.

    ---

    ## 4. Profilinformationen

    Auf Seite 4 („Profil- und Spieleinformationen“) wird dein Profil analysiert. Die ausgewählten Filter werden dabei berücksichtigt.

    ---

    ## 5. Zufällige Spielempfehlung

    Die zufällige Spielempfehlung basiert auf dem Konzept, dass analysiert wird, welche Kategorien, Genres und Tags (User-Tags, die jedes Spiel von seinen Nutzern erhält) du am meisten gespielt hast.

    Anschließend werden Spiele gefiltert, die diese Merkmale enthalten. Aus den verbleibenden Spielen werden jeweils drei Spiele ausgegeben, wenn der Button „Drück mich“ betätigt wird. Dies kann beliebig oft wiederholt werden.

    Ausgewählte Filter haben hier keinen Einfluss auf das Ergebnis.

    ---

    ## 6. Das Herz des Projekts – individuelle Spieleempfehlung

    
    ### 6.1 Profil

    Da Steam das Scrapen von Userdaten verbietet, erfolgt die Empfehlung stets auf Basis deines Profils.

    Hierzu wird ein DataFrame angezeigt, der die Mittelwerte deines Profils für alle Features, Kategorien und User-Tags enthält. Du hast die Möglichkeit, eine Gewichtung einzuführen. Das bedeutet, dass die Spielzeit deiner Spiele und somit auch die Spielzeit der Features, Kategorien und User-Tags Einfluss auf das Profil haben.

    Zusätzlich besteht die Möglichkeit, nur die letzten 14 Tage zu betrachten. Das hat den großen Vorteil, dass Spiele, die seit Jahren nicht mehr gespielt wurden, nicht berücksichtigt werden.

    Wenn du allerdings sagst: „Ich möchte nicht, dass mein Profil mit Gewichtungen verwendet wird“ oder du gezielt nach einer bestimmten Kombination von Features suchst, bietet dir die App die Möglichkeit, dein Profil manuell zu bearbeiten und damit die Empfehlung gezielt zu beeinflussen.

    
    ### 6.2 Modelle

    Hast du ein Profil erstellt und Auswahlmöglichkeiten getroffen, kannst du in der Selectbox ein Modell für die Vorhersage auswählen.

    
    #### 6.2.1 Distanzmodell (teilweise ungenau)

    Das Distanzmodell basiert auf der Kosinus-Ähnlichkeit in Kombination mit der euklidischen Distanz.

    Warum teilweise ungenau?

    Die euklidische Distanz ist hier teilweise problematisch. Wir haben 738 Features – je mehr Features, desto ungenauer wird das Ergebnis.

    Die Kosinus-Ähnlichkeit sorgt jedoch dafür, dass nur Vektoren mit ähnlicher Richtung betrachtet werden. Deshalb ist das Modell nur teilweise ungenau.

    
    #### 6.2.2 Distanzmodell in Kombination mit Reviews

    Hier werden zusätzlich Reviews der Spiele betrachtet. Ziel ist es nicht nur, ein nächstes Spiel vorzuschlagen, sondern ein gutes nächstes Spiel.

    Die Intuition dahinter ist: Die Nutzer wissen, was ein gutes Spiel ist, und diese Information nutzen wir. Damit Spiele mit wenigen Reviews nicht zu stark ausreißen und alles verzerren, muss dies angepasst werden.

    Betrachten wir nur den Anteil positiver Reviews, hätte ein Spiel mit zwei Reviews, davon zwei positiv, eine Weiterempfehlungsrate von 100 %. Das würde bedeuten, dass dieses Spiel – zumindest aus Nutzersicht – besser wäre als Counter-Strike mit über neun Millionen Reviews, von denen über sieben Millionen positiv sind. Und was ist mit Spielen, die gar keine Rezensionen haben?

    Durch das Agresti-Coull-Intervall können wir Spiele statistisch signifikanter anhand ihrer Reviews bewerten.

    Anschließend wird ein gewichteter Mittelwert aus Reviews und normalisierter euklidischer Distanz berechnet.

    Die Top-20-Spiele, die infrage kommen, werden ausgegeben. Falls ein Spiel nicht zusagt, kann ein Button gedrückt werden, um das nächste Spiel anzuzeigen.

    ---

    ## 7. Disclaimer

    Leider können nicht alle Daten behandelt werden. Aktuell gibt es das Problem das viele Spiele aus der Bibliothek nicht in den Daten enthalten sind.
    Dies kann dazu dass ein vielgespieltes Spiel nicht im Profil enthalten ist und die Empfehlung natürlich verzerrt.


"""
)