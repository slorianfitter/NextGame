# 🎮 NextGame

> Ein Projekt zur individuellen Spieleempfehlung basierend auf der eigenen Steam-Bibliothek.

---

## 📚 Inhaltsverzeichnis
1. [Warum das Projekt?](#warum-das-projekt)
2. [Was ist der Plan?](#was-ist-der-plan)
   - [1. Datenbeschaffung](#1--datenbeschaffung)
   - [2. Modell zur Vorhersage](#2--modell-zur-vorhersage)
   - [3. Frontend](#3--frontend)
3. [Aktueller Stand 10.10.2025](#-aktueller-stand-10102025)
4. [Update 16.10.2025](#-update-16102025)
5. [Update 04.11.2025](#-update-04112025)
6. [Update 19.11.2025](#-update-19112025)
7. [Update 20.11.2025](#-update-20112025)
7. [Update 24.11.2025](#-update-24112025)
8. [Update 26.11.2025](#-update-26112025)
9. [Update 28.11.2025](#-update-28112025)
10. [Update 09.01.2026](#-update-09012026)

---

## Warum das Projekt?

Ich spiele leidenschaftlich gerne Computerspiele und stehe regelmäßig vor dem Problem, **welches Spiel ich als Nächstes spielen möchte**.  
Der Markt ist riesig und wächst stetig weiter. Oft erwische ich mich dabei, wie ich endlos durch verschiedene Stores scrolle – meist ohne Erfolg.

Um meine Zeit nicht mit stundenlangem Lesen von Reviews und Beschreibungen zu verschwenden, möchte ich ein **Modell entwickeln**, das meine Spielebibliothek analysiert und mir ein Spiel vorschlägt, das **meinen individuellen Vorlieben entspricht**.

Ich bin mir noch nicht sicher, ob das Modell nur ein einzelnes Spiel oder gleich eine **Liste mit passenden Spielen** empfehlen soll. Eine Liste wäre vermutlich sinnvoller – schließlich ist der Markt groß, und es gibt selten nur eine perfekte Option.

Natürlich gibt es bereits Webseiten, die Spiele empfehlen. Der Unterschied: Diese Empfehlungen sind **allgemein** und nicht **personalisiert**.  
Red Dead Redemption 1 oder 2 zu empfehlen, ist keine Meisterleistung – das sind Spiele, die ohnehin von fast allen gelobt werden.  
Ich möchte dagegen ein System, das **meine persönliche Historie** berücksichtigt:

- Was habe ich bereits gespielt?  
- Wie lange habe ich es gespielt?  
- Welche Genres spiele ich besonders häufig?

Denn es bringt nichts, mir einen Simulator vorzuschlagen, wenn ich eigentlich leidenschaftlich gern Kampfspiele spiele.

---

## Was ist der Plan?

Ich teile das Projekt in **drei Hauptteile**:

---

### 1. 📊 Datenbeschaffung

Grundsätzlich ist es schwierig, an Spieledaten zu gelangen, da Entwickler meist kein Interesse daran haben, ihre Daten zu teilen.  
**Glücklicherweise ist Steam (Valve)** eine hervorragende Quelle: Sie erlauben Scraping und stellen **mehrere öffentliche APIs** bereit.

Für diese APIs braucht man teilweise einen **API-Key**, den sich jeder Steam-Nutzer einfach generieren kann.  
Daneben gibt es aber auch **API-Endpunkte ohne Key**, die öffentlich zugänglich sind.

Ich habe mich entschieden, mich zunächst **vollständig auf Steam-Daten** zu stützen, da:
- Steam die größte Plattform für den Kauf und das Spielen von PC-Spielen ist.
- Rund **270.000 Produkte** im Store gelistet sind (wovon ca. 20–40 % tatsächliche Spiele sind – *eigene Schätzung, wird nach Abschluss der Datenbeschaffung verifiziert*).
- Nutzer ihre eigenen **Spielzeiten und Bibliotheken per JSON abrufen** können.
- Öffentliche Profile auch **fremde Spielzeiten einsehbar** machen.

Zusätzlich möchte ich auch **Reviews** einbeziehen – sowohl die **All-Time-Bewertungen** als auch die **Reviews der letzten 30 Tage**, um aktuelle Trends zu erkennen.

---

### 2. 🧠 Modell zur Vorhersage

Damit das Modell funktioniert, brauche ich verschiedene Datenpunkte – insbesondere:
- Anzahl der Reviews  
- Spielzeit  
- Genres und Kategorien  

Diese Daten reichen zunächst, um eine **Baseline** zu erstellen.  
Mein erster Ansatz ist ein **Vergleichsmodell**, da:
- das Modell simpel ist,  
- es sich gut anpassen lässt,  
- und es gleich eine Liste von Spielen liefert, die potenziell gut passen könnten.

Das **Baseline-Modell** hat jedoch auch Nachteile:
- Die Rückgabeliste kann sehr lang und ungenau werden.

Langfristig möchte ich daher ein **komplexeres Modell** entwickeln, das bereits über einen gespeicherten Spielekatalog verfügt und mit meinen Eingaben effizient arbeitet.  
Wie genau das umgesetzt wird, ist aktuell noch in Planung.

---

### 3. 💻 Frontend

Für den Nutzer soll es so einfach wie möglich sein:  
Idealerweise kann man **per Drag & Drop oder Copy & Paste** seine Spieldaten einfügen und bekommt anschließend **eine schön aufbereitete Empfehlung** mit Bild, Titel und Beschreibung.

Mein Ziel ist es, **nicht nur ein funktionales Modell**, sondern auch eine **ansprechende Benutzeroberfläche** zu entwickeln.  
Das soll mich selbst fordern und mir helfen, neue Technologien zu lernen.

Ein geplanter Zusatz ist ein **„Ablehnen“-Button**, falls ein vorgeschlagenes Spiel nicht gewünscht ist.  
Das ist wichtig, da viele Spieler – mich eingeschlossen – auf **mehreren Plattformen** spielen (z. B. PC, Xbox, PlayStation).  
Wenn ich ein Spiel also schon auf einer anderen Plattform gespielt habe, soll es **abgelehnt und durch eine neue Empfehlung ersetzt** werden.

---

## 📍 Aktueller Stand 10.10.2025

Momentan befinde ich mich in der **Datenbeschaffungsphase**.  
Die Skripte sind geschrieben und laufen bereits seit rund zwei Tagen kontinuierlich.

### Aktuelles Problem

Steam reagiert nicht besonders begeistert, wenn ich **gleichzeitig API-Anfragen** stelle und **den Store nach Reviews abfrage** – das führte bisher zu **mehrstündigen Timeouts**.

Deshalb beschaffe ich die Daten nun **sequenziell**, also nacheinander.  

Der aktuelle Ablauf:
1. Spiele werden von Nicht-Spielen (z. B. DLCs, Add-ons) gefiltert.  
2. Pro Spiel-ID werden Daten abgefragt.  

Das Ganze dauert etwa **vier Tage**, da:
- Steam bei API-Keys **100.000 Anfragen pro Tag** erlaubt.  
- Ich derzeit eine API **ohne Key** nutze, die anscheinend andere Limits hat.  

Nach meinen Tests liegt der **Sweet Spot** bei etwa **40 Anfragen pro Minute** – das ergibt ca. **57.000 Anfragen pro Tag**,  
was wiederum rund **4,5 Tage** für alle 270.000 IDs bedeutet.  
Danach müssen noch die restlichen Spieldaten ergänzt werden, was ebenfalls mehrere Tage in Anspruch nehmen wird.

---

## 📆 Update 16.10.2025

Die ganzen AppIDs sind nun alle abgeklappert und ich habe etwas mehr als 100 Tausend Spiele identifizieren können. 

Bei der Datenaufbereitung sind mir allerdings viele Probleme aufgefallen:
- rund 100 Tausend Zeilen NAs -> bedeutet, mein Skript war nicht sehr sicher und hat deutliche Lücken.  
- Weil das Skript solche Lücken hat, muss ich das Ganze jetzt nochmal machen.  
- Steam ist leider nicht so einheitlich, wie ich es gerne hätte.

Das Ganze ist mir nämlich aufgefallen durch die NAs bei der Altersbeschränkung. Neben den klassischen Werten wie 0, 6, 12 usw. kamen auch Strings und die positive Grenze von Int64 heraus.  
Damit ein Spiel in Deutschland sichtbar ist, muss es eine Altersbeschränkung geben. Entweder von USK oder von Steam selbst.  
Mein Code war diesbezüglich nicht robust. Ich habe nur gecheckt, ob ein Item im JSON enthalten ist, nicht, ob es leer ist – mein Fehler.

Ein Fehler, der jetzt leider schmerzt, weil ich dick hinter meinem eigenen Zeitplan liege.

---

### 🛫 Plan für die kommenden Tage

- Code nochmal anpassen, robuster und effektiver  
- Die fehlenden Daten nochmals beschaffen  
- Daten aufbereiten  

Sobald diese drei Unterpunkte erledigt sind, werde ich nochmals ein Update schicken und das weitere Vorgehen niederschreiben.

Das Ganze ist sehr ärgerlich, aber nicht schlimm, weil ich aus Fehlern lerne und nun weiß, dass ich in Zukunft robuster programmieren muss.

---

## 📆 Update 04.11.2025

Ich habe begonnen, ein **Interface mit Streamlit** zu entwickeln, um die Nutzerdaten übersichtlich darzustellen.  
Das grundlegende **Streamlit-Interface steht bereits**, benötigt aber noch **Feinschliff im Design**.  
Ebenso muss das Skript später angepasst werden, sobald alle Modelle stehen und weitere Daten vorliegen.


---

### 💭 Aktuelle Gedanken

Ich plane aktuell, **drei Modelle** zu implementieren:

#### 🔹 Modell 1 – Basismodell
Ein einfaches Modell, das eine Liste von Spielen aus dem **meistgespielten Genre** vorschlägt.

#### 🔹 Modell 2 – Distanzmodell
Ein Modell, das **Abstände zwischen Spielen** misst.  
Ich bin mir noch nicht sicher, ob ich dafür einen **k-NN-Algorithmus** oder **K-Means** verwenden werde.  
Ziel ist es, **ähnliche Spiele zu identifizieren**, basierend auf:
- Genre  
- Kategorien  
- User-Tags  

#### 🔹 Modell 3 – Erweiterung von Modell 2
Dieses Modell soll zusätzlich auch **Reviews** mit einbeziehen.  
Reviews sind zwar subjektiv, aber bei einer großen Menge lässt sich ein **klarer Trend** erkennen.  
Das Ziel ist eine **realistische, personalisierte Prognose**, die den Nutzer optimal zufriedensellt.

---

### ✅ Fertige Gedanken

Das erste Modell ist bereits **fertiggestellt**.  
Es handelt sich um ein **Basismodell**, das das meistgespielte Genre auswählt und eine **Liste von 10 zufälligen Spielen** dieses Genres vorschlägt.

**Folgen:**
- Das Modell ist **nicht präzise**,  
- bietet aber dafür **viel Abwechslung** in den Vorschlägen.

Beispielsweise wählt es beim Genre *Action* aus rund **35.000 Spielen** aus.

---

### 🏁 Weitere Fortschritte

Neben dem Modell habe ich einen **HTML-Scraper** geschrieben, der mir:
- **Reviews**,  
- **Tags**  
- und **Preise**  

automatisch beschafft.

Die **Preise** dienen als Kontrolle, falls im JSON der Steam-API fehlerhafte Werte stehen.  
**Reviews** und **Tags** werden für Modell 2 und 3 benötigt.

Da jede **Shopseite einzeln aufgerufen** werden muss, dauert das Sammeln der Daten entsprechend lange:  
- Aktuell hole ich **ein Request alle zwei Sekunden**.

Ein ärgerlicher Fehler war, dass ich **anfangs die Tags nicht mitgescraped** habe.  
Dadurch musste ich die vorherige Beschaffung abbrechen und **von vorne beginnen** – ein klassischer, aber lehrreicher Rückschlag.

---

### 🛫 Plan für die kommenden Tage (Part 2)

- Das **Distanzmodell** schreiben und erste Tests durchführen  
- Eventuell das **Distanzmodell direkt im Streamlit-Interface** implementieren  
- Parallel weiterhin Daten beschaffen (**Tags**, **Reviews**, **Preise**)  
- **Design-Feinschliff** im Streamlit-Frontend 

---

## 📆 Update 19.11.2025

Das Projekt ist so gut wie abgeschlossen.  
Alle bislang notwendigen Daten sind bereits seit einer Woche vollständig erhoben und bearbeitet. Es benötigt nur noch einen Feinschliff der Labels und Korrektur kleinerer Tippfehler.

### 🔹 Modell 1
Modell 1 steht seit Wochen und funktioniert wie geplant.  

### 🔹 Modell 2
Modell 2 wurde vorgestern fertiggestellt und hat einige Schwierigkeiten verursacht.  
Der Grundansatz war ein einfaches Distanzmaß zwischen Spielen. Ein sehr naiver Ansatz, der theoretisch funktioniert, hier aber aufgrund der Binärdaten nicht optimal war.  

Das Distanzmodell berücksichtigt nicht nur die euklidische Distanz zwischen den Spielemerkmalen, sondern filtert vorher auch den Winkel der Vektoren. Dadurch können ähnliche Spiele zum aktuellen Nutzerprofil identifiziert werden.  

Zusätzlich habe ich es dem Nutzer ermöglicht, sein Profil einzusehen und bei Bedarf zu bearbeiten. Die genauen Instruktionen für das Profil müssen allerdings noch in das Interface implementiert werden.  

Insgesamt liefert das Modell jedoch solide Ergebnisse, und ich bin vorerst zufrieden.

### 🔹 Modell 3
Modell 3 befindet sich noch in der Entwicklung. Ziel ist, die **Reviews** zusätzlich zu berücksichtigen. Dabei habe ich bisher einige Herausforderungen festgestellt:

- 75 % aller Spiele haben weniger als 130 Reviews. Das bedeutet nicht, dass sie schlechte Spiele sind.  
- Klassische Ansätze wie:
  - positive Reviews / Gesamtanzahl der Reviews → starke Verzerrung bei Spielen mit wenigen Reviews  
  - positive Reviews − negative Reviews → ermöglicht, dass kleine Spiele negativ dominieren
    
  führen zu Problemen.

**Lösungsansätze**, die ich nun testen möchte:

- Wilson Lower Bound  
- Bayesian Weighted Rating  
- Wald-Intervall  
- Agresti-Coull-Intervall  

Ziel ist es, die Methode zu finden, die am sinnvollsten Ergebnisse liefert.  
Außerdem wird weiterhin nach anderen Methoden Ausschau gehalten.


### 🛫 Nächste Schritte
- Implementierung der Grundzüge von Model 3  
- Testen verschiedener Methoden zur Berechnung von Bewertungen basierend auf Reviews  
- Feinschliff im Interface, insbesondere für die Profilbearbeitung

 
- Mit den **Grundzügen des dritten Modells** beginnen

---

## 📆 Update 20.11.2025

Die Modelle stehen.  
Ich habe mich für das **Agresti–Coull-Konfidenzintervall** entschieden.  
**Bayesian** und **Wilson** wären ebenfalls geeignete Alternativen.  
Das **Wald-Intervall** ist hingegen für Spiele mit wenigen Reviews ungeeignet und liefert zu ungenaue Ergebnisse.

Gestern ist mir außerdem aufgefallen, dass ich durch einen Fehler meine lokalen Daten mit dem Stand aus dem Repo vom **04.11.** überschrieben habe.  
Dadurch fehlen mir einige Informationen, und beim Main-Skript bin ich damit wieder auf dem Stand von vor zwei Wochen.

Inzwischen habe ich jedoch viel aufgeholt und bin wieder auf Kurs.  
Mit Ausnahme der Reviewdaten ist alles wieder in einem normalen Zustand.


### 🛫 Nächste Schritte

- weiter coden  
- Krone richten, Zacken austauschen und aus dem Fehler lernen. 

---

## 📆 Update 24.11.2025

Das Projekt steht nun auf eigenen Füßen. Das Interface steht und es funktioniert erstmal so, wie ich es mir vorstelle. 
Natürlich gibt es noch Anpassungen und verbesserungsmöglichkeiten. Dazu aber später mehr im Projektoverview.

Nun werde ich das Projekt nach Github klonen und mit Streamlitcloud verbinden, damit das Projekt jederzeit abrufbar ist und getestet werden kann.

---

## 📆 Update 26.11.2025

Vorgestern habe ich das Repository geklont und anschließend versucht, es mit Streamlit Cloud zu verbinden. Grundsätzlich klappt die Verbindung, die App wird auch angezeigt, aber sie läuft nicht.

Vermutlich liegt das Problem an der Größe der App. Zunächst hatte ich angenommen, dass die Abhängigkeiten nicht korrekt sind, aber in diesem Fall würde ich eine entsprechende Fehlermeldung bekommen – die trat jedoch nicht auf.

Also muss ich mir zunächst eine alternative Lösung überlegen.
Lokal (Localhost) funktioniert die App dagegen einwandfrei.


## 📆 Update 28.11.2025

Das Projekt ist nun **vorzeigbar**.  

### Aktueller Stand

- Die App läuft jetzt über **Hugging Face** (https://huggingface.co/spaces/slorianfitter/newgame), auch wenn der Upload von Dateien blockiert ist. 
 
- Lokal funktioniert die App weiterhin problemlos, und über Hugging Face ist zumindest eine funktionierende Version mit den lokalen Daten verfügbar.  
- Es gibt insgesamt **fünf relevante CSV-Dateien**, von denen eine selbst beschafft werden muss, die restlichen können direkt genutzt werden.  
- Damit kann das Dashboard und die Modelle lokal verwendet werden.  

### Wichtige Hinweise

- Der Punkt, an dem der Nutzer den eigenen **Steam-API-Key** eingeben muss, wird noch angepasst.  
- Durch unvollständige Steam-Daten fehlen manche Spiele in der Analyse. Ein Beispiel: **NBA 2K21** ist im Shop sichtbar, aber nicht in den Steam-IDs enthalten. Solche Fälle können aktuell nicht berücksichtigt werden.  
- Weiterhin werden alle Spiele herausgefiltert, die keine Altersbeschränkung haben – auch Spiele aus der eigenen Bibliothek. 
- Geplant ist, **Kontakt mit Steam** aufzunehmen, um zu klären, warum einige Daten fehlen.  

### 🛫 Nächste Schritte

- Projektübersicht erstellen und alle bisherigen Fortschritte dokumentieren.  
- Machine Learning testen – auch wenn die ursprüngliche Idee vorerst verworfen wurde, möchte ich es dennoch ausprobieren.  
- Datenaktualisierung und Profilintegration verbessern, sodass auch Spiele außerhalb der aktuellen Steam-IDs berücksichtigt werden können.  
- Nach alternativen Lösungen suchen, um die App für den Nutzer einfacher und komfortabler zu machen.

## 📆 Update 09.01.2026

Die App hat jetzt ein neues Layout bekommen. Inzwischen sind es mehrere Seiten, statt eine einzige. Dadurch ist alles viel kompakter und Übersichtlicher. Beim Start der Seite werden jetzt per Funktion die Daten in den Cache geladen.
Wenn der User seine Daten hochlädt werden diese Ebenfalls in den Cache geladen. Dadurch kann bequem durch die Seiten geklickt werden, ohne dass Informationen verloren gehen. 
Insgesamt ist die App nun viel schneller und angenehmer zu nutzen

Ein Nutzungsinfo ist ebenfalls implementiert und ist die Startseite der App.

Machine Learning selbstn konnte nicht implementiert werden. Es lohnt sich einfach überhaupt nicht, denn ich habe keine Profildaten - außer meine eigenen:

- Natürlich könnte man hier eigene Profile ersetllen und dann einen ähnlichen algorithmus anwenden wie Netflix oder Spotify es tun, aber die Daten wären nicht für reelle Szenarien anwendbar und somit nicht nutzbar.
- Supervised Learning funktioniert sowieso schon nicht und unsupervised Learning aufgrund der fehlenden Profilinformationen auch nicht.
- Ebenfalls habe ich überlegt vielleicht über die Cover der Spiele ein CNN zu starten, lohnt aber auch nicht, denn das Cover muss nicht unbedingt das Gameplay widerspiegeln

Fazit: Machine Learning lohnt nicht. Zumindest nicht traditionelles lernen.


Ich habe den Main Code und die Funktionen angepasst. Sie sollten nun leserlicher sein und deutlich mehr Kommentare umfassen. Gleichzeitig habe ich einige Bugs gefixt.
Für die Datenbeschaffung Skripte ist die für Ende Januar ebenfalls geplant. 
Kontakt mit Steam habe ich nicht aufgenommen. Stattdessen habe ich vorgestern nochmal die steamids per api abgefragt. Inzwischen sind es rund 150 Tausend Spiele. Ende Januar werde ich diesbezüglich alle Daten nochmals aktualisieren.





