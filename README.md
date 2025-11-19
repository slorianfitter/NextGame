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



