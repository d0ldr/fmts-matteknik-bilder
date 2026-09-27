Karakteristisk impedans
Nedan är helt genererad av Claude.

Ja! Det svåra för nybörjare är att 50 Ω *inte* är ett motstånd man kan mäta med en multimeter. Mäter du på en 50 Ω-koaxkabel med en ohmmeter får du "oändligt" (öppen krets) mellan innerledare och skärm. Så man behöver bygga upp förståelsen i några steg.

**1. Den oändligt långa kabeln (kärnexemplet)**

Tänk dig en koaxkabel som är oändligt lång. Du kopplar en spänningskälla i ena änden. Vad händer?

En vågfront börjar vandra längs kabeln. För varje centimeter vågen avancerar måste kabelns kapacitans laddas upp, och det kräver ström. Eftersom kabeln aldrig tar slut kommer källan att fortsätta leverera en *konstant* ström så länge vågen vandrar. Källan "ser" alltså ett förhållande mellan spänning och ström, precis som om den vore kopplad till ett motstånd:

> Z₀ = U / I för en våg som vandrar längs kabeln

För en 50 Ω-kabel: lägger du på 5 V flyter det 100 mA. Men ingen energi omvandlas till värme i kabeln, den transporteras bara iväg.

Poängen: **karakteristisk impedans är det motstånd en våg "känner" när den färdas längs ledningen**, inte ledningens resistans.

**2. Vad bestämmer värdet?**

Bara kabelns geometri och isolermaterial, inte längden. Tjockare innerledare eller tunnare isolering ger mer kapacitans och lägre Z₀. Formeln är

> Z₀ = √(L/C)

där L och C är induktans och kapacitans per meter. En meter och en kilometer av samma kabel har samma Z₀.

**3. Varför det spelar roll: reflektioner**

Här passar en analogi med ett rep bra. Skicka en puls längs ett rep:

- Är repet fastknutet i ett likadant rep fortsätter pulsen utan att märka skarven (**anpassad last**, 50 Ω i änden).
- Är repet fastspikat i en vägg studsar pulsen tillbaka upp och ner (**kortslutning**).
- Hänger repet fritt studsar pulsen tillbaka åt samma håll (**öppen ände**).
- Övergår det i ett tjockare eller tunnare rep studsar en *del* av pulsen (**felanpassning**).

Om kabeln avslutas med ett 50 Ω-motstånd tar motståndet emot vågen exakt som om kabeln fortsatte i oändlighet, och inget reflekteras. Därför har oscilloskop ofta ett valbart 50 Ω-ingångsläge, och därför sätter man termineringar på signalgeneratorer.

Ett bra demoexperiment om ni har utrustning: skicka en snabb puls i en lång koaxkabel (några meter räcker) och mät på oscilloskopet med öppen ände, kortsluten ände och 50 Ω-terminering. Man ser reflexen komma tillbaka, vänd eller inte vänd, eller försvinna helt.

**4. Varför just 50 Ω?**

Det är en kompromiss. För en luftisolerad koaxkabel ger ungefär 30 Ω högst effekttålighet och ungefär 77 Ω lägst förluster. 50 Ω ligger mittemellan och blev standard inom mätteknik och radio. (TV-antennkabel använder 75 Ω, där låga förluster väger tyngre.)

**En mening att avsluta med:**
*Karakteristisk impedans är förhållandet mellan spänning och ström i en våg som vandrar längs en ledning. Den bestäms av ledningens geometri, och om lasten i änden har samma värde försvinner vågen in i lasten utan att studsa tillbaka.*

Vill du att jag gör en Beamer-frame med en TikZ-figur av detta, till exempel repanalogin eller en puls som reflekteras vid öppen, kortsluten och anpassad ände?