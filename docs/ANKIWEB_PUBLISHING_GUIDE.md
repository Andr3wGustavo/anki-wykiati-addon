# 🚀 Guia Oficial de Publicação no AnkiWeb
## Anki Wykiati Toolkit (Discord Image Ingestion & AMOLED Theme Studio)

Este guia prático e didático explica o passo a passo completo para você publicar o **Anki Wykiati Toolkit** no portal oficial do **AnkiWeb**, permitindo que milhares de estudantes de medicina, tecnologia e idiomas baixem e atualizem o seu plugin com um único código numérico (ex: 2049182371).

---

## 📦 1. O Pacote de Distribuição (.ankiaddon)

O arquivo .ankiaddon é o formato padrão oficial do AnkiWeb (internamente é um arquivo .zip estruturado com o manifesto, código e configurações).

### Como Gerar a Versão Mais Recente:
No terminal da raiz do projeto, execute:
`ash
python package_addon.py
`
O script empacotará automaticamente todos os arquivos essenciais e gerará o arquivo pronto em:
`	ext
release/anki-discord-toolkit.ankiaddon
`

---

## 🌐 2. Passo a Passo no AnkiWeb

1. **Acesse o Portal de Compartilhamento do AnkiWeb:**
   - Faça login na sua conta em https://ankiweb.net.
   - Vá para o menu de **Add-ons** ou acesse diretamente: https://ankiweb.net/shared/addons/.
   - Clique no botão **Share an Add-on** (Compartilhar um Add-on).

2. **Envio do Arquivo (.ankiaddon):**
   - No campo de upload, selecione o arquivo gerado:  
     elease/anki-discord-toolkit.ankiaddon

3. **Preenchimento das Informações:**
   - **Title (Título):**  
     Anki Wykiati Toolkit - AMOLED Black Theme, Discord Bot & Smart Image Ingestion
   - **Supported Anki Versions (Versões Suportadas):**  
     Selecione 2.1.50+ (ou 23.10+ / 24.04+ / Qt6). Nosso código suporta nativamente PyQt6 e PyQt5 de forma não-destrutiva.

---

## 📝 3. Modelo de Descrição Pronto para o AnkiWeb (HTML)

Copie e cole o texto HTML abaixo diretamente no campo de **Description** do AnkiWeb:

`html
<h2>✨ Anki Wykiati Toolkit — The Ultimate Workflow & Aesthetic Add-on</h2>
<p>
<b>Anki Wykiati Toolkit</b> supercharges your flashcard creation with real-time Discord image auto-ingestion, 
on-demand channel synchronization, lossless WebP media compression, and a gorgeous, ultra-responsive AMOLED Full Black theme studio with intelligent WCAG light/dark contrast adaptation.
</p>

<hr/>

<h3>🔥 Key Features</h3>
<ul>
  <li><b>📥 Automated Discord Image Ingestion:</b> Post images in your Discord study channels and watch them instantly turn into visual flashcards in Anki without leaving your chat.</li>
  <li><b>⚡ One-Click On-Demand Sync:</b> Pull up to 50 recent images from any Discord channel with built-in SHA-256 cryptographic anti-duplication.</li>
  <li><b>🖼️ In-Memory WebP Image Optimizer:</b> Automatically downscales 4K photos to 1920px and converts heavy PNGs to lightweight WebP at 85% quality, saving up to 85% disk space and speeding up mobile sync.</li>
  <li><b>🎨 Deep AMOLED Black & RGB Theme Studio:</b> Choose any custom background RGB color with our interactive color wheel. Fonts, borders, and tables automatically adapt their contrast (dark/light) so text is always 100% crystal clear.</li>
  <li><b>🗂️ Smart Deck Routing:</b> Automatically route images and notes to specific sub-decks based on tags or channel origin.</li>
  <li><b>🌐 Local HTTP Bridge Server:</b> Integrated REST API (port 8765) allowing scripts, browser extensions, and webhooks to push cards directly into Anki.</li>
</ul>

<hr/>

<h3>⚡ Quick 1-Minute Setup</h3>
<ol>
  <li>Open Anki and go to <b>Tools &gt; Wykiati Toolkit &gt; Discord &amp; Image Settings</b>.</li>
  <li>Enter your Discord Bot Token and Channel ID.</li>
  <li>Click <b>📥 Pull Recent Discord Images Now</b> to import recent diagrams directly into your chosen deck!</li>
</ol>

<hr/>

<h3>💎 Source Code &amp; Issues</h3>
<p>
Open source on GitHub: <a href=https://github.com/Andr3wGustavo/anki-wykiati-addon>https://github.com/Andr3wGustavo/anki-wykiati-addon</a>
</p>
`

---

## 🔄 4. Como Funcionam as Atualizações

Quando você publicar uma nova versão:
1. Basta executar python package_addon.py.
2. Acessar a página do seu add-on no AnkiWeb e clicar em **Upload New Version**.
3. Todos os usuários que têm o seu plugin instalado receberão a atualização automaticamente ao clicar em **Tools > Add-ons > Check for Updates** dentro do Anki!

---

## 🏷️ 5. Tags Recomendadas para o AnkiWeb

Adicione as seguintes tags no campo de busca do AnkiWeb para maximizar downloads orgânicos:
- discord
- dark mode
- moled
- image
- utomation
- 	heme
- sync
- productivity
