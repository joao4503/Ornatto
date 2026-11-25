"""Gera programacao.html (e depois o PDF via Playwright) a partir dos dados abaixo.
Uso: python3 gerar_programacao.py  ->  programacao.html
"""
import html, pathlib, re

AQUI = pathlib.Path(__file__).parent
css = re.search(r"<style>(.*?)</style>", (AQUI / "programacao.html").read_text(), re.S).group(1)
css += """
td.mec { color: var(--salvia); font-size: 8.4pt; }
table:not(.perfis) td { padding-top: 1mm; padding-bottom: 1mm; }
h2 { margin-top: 0; }
.novo { display:inline-block; font: 700 6.8pt "Inter"; color: var(--dourado); border: .7pt solid var(--dourado); border-radius: 2mm; padding: 0 1.2mm; margin-left: 1.5mm; vertical-align: 1px; }
table.perfis td { font-size: 8.4pt; padding: 1.4mm 2mm; }
table.perfis td:first-child { font-weight: 600; }
.licoes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3.5mm; }
.licao { background:#fff; border:.7pt solid var(--bege); border-radius: 2mm; padding: 3mm 3.5mm; font-size: 8.6pt; }
.licao b { display:block; font: 700 10pt "Playfair"; margin-bottom: 1mm; }
.nota { font-size: 7.8pt; color: var(--salvia); margin-top: 2mm; }
"""

TAG = {"C": '<span class="tag car">Carrossel</span>', "R": '<span class="tag reel">Reel</span>',
       "S": '<span class="tag sto">Stories</span>', "L": '<span class="tag live">Ao vivo</span>'}

# (dia, hora, formato, tema/gancho, mecânica, status, estrela, novo, destaque)
SEMANAS = [
 ("Semana 1", "Natal e lançamento do sorteio", [
  ("Seg 30", "12h", "C", 'Presente de Natal · "O presente de quem sabe a diferença"', "Presente + prazo real", "pend:Fotos das latas", 0, 0, 0),
  ("Ter 01", "19h", "R", 'Série "Nem todo grão", ep. 1: a máquina · "Esse grão foi reprovado em milésimos de segundo."', "Satisfatório + som real + loop", "pend:Gravar 27/11", 1, 0, 0),
  ("Qua 02", "12h", "C", 'Guia de presentes · "Qual café combina com quem você ama?"', "Feito para enviar", "ok:Pronto", 0, 0, 1),
  ("Qua 02", "19h", "C", '<b>Lançamento do sorteio</b> · "O kit do café campeão"', "Prêmio + participação", "pend:Foto do kit 02/12", 0, 0, 1),
  ("Qui 03", "12h", "R", 'O barulho do provador · "Não, ele não está sem educação."', "Quebra de expectativa + humor", "pend:Gravar", 1, 0, 0),
  ("Sex 04", "12h", "C", 'Do cafezal à xícara · "6 etapas que ninguém vê antes da sua xícara"', "Bastidor nunca visto", "A produzir", 0, 0, 0),
  ("Sáb 05", "19h", "R", 'A saca de R$ 50 mil + sorteio · "Essa saca foi vendida por 50 mil reais."', "Número chocante + virada", "pend:Gravar", 1, 0, 0),
  ("Dom 06", "11h", "R", 'Um dia na Fanadinho, ep. 1 · rosto da marca mostrando a rotina, com humor', "Pessoa real + rotina", "pend:Gravar", 0, 1, 0),
 ]),
 ("Semana 2", "Origem, lotes e prazo dos kits (até 10/12)", [
  ("Seg 07", "19h", "C", 'Ficha sensorial · "O número que diz se seu café é especial"', "Chute antes de arrastar", "A produzir", 0, 0, 0),
  ("Ter 08", "12h", "R", 'Do grão à xícara · "Nem todo grão chega até aqui."', "Peça de marca", "ok:Pronto", 0, 0, 0),
  ("Qua 09", "12h", "C", 'Tropical da Chapada · "Esse café tem gosto de maracujá. Sério."', "Afirmação que parece mentira", "A produzir", 0, 0, 0),
  ("Qui 10", "12h", "C", '<b>Última chamada dos kits</b> · "Hoje é o último dia"', "Prazo real", "ok:Pronto", 0, 0, 1),
  ("Qui 10", "19h", "R", 'Gosto de maracujá · "E ninguém colocou maracujá nele."', "Reação na prova", "pend:Gravar", 1, 0, 0),
  ("Sex 11", "19h", "C", 'Por que café especial custa mais? · "Um pacote de 250 g começa com 312,5 g de café verde."', "Esforço que justifica o preço", "A produzir", 0, 1, 0),
  ("Sáb 12", "12h", "R", '3 erros com café em casa · "Você pode estar estragando um café especial."', "Erro comum, fácil de entender", "pend:Gravar", 0, 0, 0),
  ("Dom 13", "11h", "R", 'Um dia na Fanadinho, ep. 2', "Série com o rosto da marca", "pend:Gravar", 0, 1, 0),
 ]),
 ("Semana 3", "Cafeterias (rota do Alex de 14 a 18/12)", [
  ("Seg 14", "12h", "C", 'Para cafeterias · "Sua cafeteria serve café ou serve história?"', "Pergunta direta ao dono", "A produzir", 0, 0, 0),
  ("Ter 15", "19h", "R", 'Teste cego · "Dei dois cafés sem dizer qual era qual."', "Reação real + revelação", "pend:Gravar", 1, 0, 0),
  ("Qua 16", "19h", "C", 'Flor de Laranjeira · "90 pontos. Dá para sentir a flor."', "Sensorial + panetone", "A produzir", 0, 0, 0),
  ("Qui 17", "12h", "R", 'Mito ou verdade · "Café bem escuro é mais forte?"', "Times nos comentários", "pend:Gravar", 0, 0, 0),
  ("Sex 18", "12h", "C", 'Rebenefício · "4 máquinas que reprovam o seu café"', "Bastidor + série", "A produzir", 0, 0, 0),
  ("Sáb 19", "19h", "R", 'Ep. 2 da série: o som da torra · "Esse é o som do café ficando pronto."', "Som real + loop", "pend:Gravar", 0, 0, 0),
  ("Dom 20", "11h", "R", 'Tipos de gente tomando café na ceia · esquete com a equipe', "Humor: marcar alguém", "pend:Gravar", 0, 1, 0),
 ]),
 ("Semana 4", "Ceia, sorteio e recesso (24 e 25/12)", [
  ("Seg 21", "12h", "C", 'Café da ceia · "O café que vai roubar a cena na ceia" (harmonizações das fichas)', "Para salvar e enviar", "A produzir", 0, 0, 0),
  ("Ter 22", "19h", "L", '<b>Sorteio ao vivo</b> e anúncio do ganhador', "Evento ao vivo", "", 0, 0, 1),
  ("Qua 23", "19h", "C", 'Quem faz a Ornatto · "Por trás de cada pacote"', "Rostos e funções", "A produzir", 0, 0, 0),
  ("Qui 24", "", "S", 'Agendado: enquete "Qual café vai na sua ceia?"', "Interação", "", 0, 0, 0),
  ("Sex 25", "10h", "C", 'Agendado: Feliz Natal · "De nós para você" + aviso do recesso', "Cartão para enviar", "A produzir", 0, 0, 0),
  ("Sáb 26", "19h", "R", 'Respondendo comentários · a melhor pergunta em 30 s', "Resposta a comentário", "pend:Gravar", 0, 0, 0),
  ("Dom 27", "11h", "R", '2026 em 20 segundos · prêmios, leilão, Coffee of the Year, equipe', "Retrospectiva rápida", "A produzir", 0, 1, 0),
 ]),
]

PERFIS = [
 ("Filipe Galle (ES)", "Produtor de conilon", "~308 mil no Instagram e ~555 mil no TikTok", "1 vídeo por dia", "Esquetes de humor sobre a rotina na roça", "Personagens fixos, situação do dia a dia, humor", "Série com rosto fixo e rotina"),
 ("Kassiane Thayna (MG)", "Agricultora, hoje com marca própria", "~3 milhões somando as redes (imprensa)", "Não verificado", "Colheita manual na lavoura de morro", "\"Como é difícil colher café\", esforço real, humor", "Mostrar o trabalho por trás do grão (colheita de 2027)"),
 ("Felipe Brazza (MG)", "Cafeicultor, barista e mestre de torra", "~60 mil (imprensa, data incerta)", "Não verificado", "Café especial explicado de forma simples; seleção de grãos", "Desmistificar", "Educação curta, sem jargão"),
 ("Ana Carolina Malta (MG)", "Cafeicultora", "~9 mil", "Não verificado", "Instagram como \"sala de aula\" de café especial", "Ensinar quem está começando", "Conteúdo de salvar que vira venda"),
 ("Morgan Eckroth (EUA)", "Barista campeã", "~6 milhões no TikTok", "Não verificado", "Esquetes de cafeteria (barista × cliente)", "Humor de situação + técnica", "Esquete \"tipos de gente tomando café\""),
 ("James Hoffmann (Reino Unido)", "Campeão mundial de barista", "+2 milhões no YouTube", "Não verificado", "Testes e comparações", "Curiosidade + rigor, sem precisar saber de café", "Testes (teste cego, torra clara × escura)"),
]

LICOES = [
 ("Pessoa real ganha de peça de marca", "Os casos que mais viralizaram no café brasileiro têm alguém falando com a câmera, na roça, com humor."),
 ("Constância vence o vídeo perfeito", "Filipe Galle publica um vídeo por dia. Série fixa e frequência criam hábito no público."),
 ("O esforço vende o preço", "Mostrar o trabalho por trás do grão justifica o preço do café especial."),
 ("Não exigir conhecimento", "Os vídeos que se espalham são entendidos por quem não sabe nada de café."),
 ("Envio pesa mais que curtida", "Segundo Mosseri, chefe do Instagram, o que mais leva a quem não segue é o envio por direct, além do tempo assistido. Por isso, terminar pedindo um envio."),
 ("Original sempre", "Desde 2026, contas que repostam conteúdo alheio perdem recomendação. Fotos de clientes ficam nos stories, não no feed."),
]

def status(s):
    if s.startswith("pend:"): return f'<span class="pend">{s[5:]}</span>'
    if s.startswith("ok:"): return f'<span class="ok">{s[3:]}</span>'
    return s

def tabela(rows):
    out = ['<table><colgroup><col style="width:15mm"><col style="width:10mm"><col style="width:21mm"><col><col style="width:50mm"><col style="width:30mm"></colgroup>',
           '<tr><th>Dia</th><th>Hora</th><th>Formato</th><th>Tema · gancho</th><th>Por que viraliza</th><th>Status</th></tr>']
    for d, h, f, t, m, s, star, novo, dest in rows:
        tag = TAG[f] + (' <span class="star">★</span>' if star else "")
        t2 = t + ('<span class="novo">NOVO</span>' if novo else "")
        out.append(f'<tr{" class=\"dest\"" if dest else ""}><td class="dia">{d}</td><td class="hora">{h}</td><td>{tag}</td><td>{t2}</td><td class="mec">{m}</td><td>{status(s)}</td></tr>')
    out.append("</table>")
    return "\n".join(out)

def cab(titulo, sub):
    return f'<header><div><h1>{titulo}</h1><p class="sub">{sub}</p></div><img src="assets/logotipo-verde-dourado.svg"></header>'

def rod(n, total, txt="★ maiores apostas · publicadas primeiro como reel de teste, com gancho A e B · NOVO = entrou nesta versão"):
    return f'<div class="rodape"><span>{txt}</span><span>Ornatto Cafés Especiais · {n}/{total}</span></div>'

T = 5
pags = []
# Página 1: análise do nicho
p = [cab('O que viraliza no <em>nosso nicho</em>', 'Perfis de café que cresceram no Instagram e no TikTok, e o que a Ornatto aproveita de cada um')]
p.append('<table class="perfis"><colgroup><col style="width:34mm"><col style="width:34mm"><col style="width:40mm"><col style="width:22mm"><col><col><col style="width:46mm"></colgroup>')
p.append('<tr><th>Perfil</th><th>Quem é</th><th>Tamanho (aprox.)</th><th>Frequência</th><th>Conteúdo</th><th>Gancho e mecânica</th><th>O que a Ornatto usa</th></tr>')
for r in PERFIS:
    p.append("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
p.append("</table>")
p.append('<h2>6 lições <span>aplicadas na programação</span></h2><div class="licoes">')
for t, d in LICOES:
    p.append(f'<div class="licao"><b>{t}</b>{d}</div>')
p.append("</div>")
p.append('<p class="nota">Números tirados de reportagens e páginas públicas encontradas em busca na web, com datas variadas. Não foi possível abrir os perfis para contar posts e visualizações. Frequência só confirmada para Filipe Galle (entrevista). Fontes: Folha Vitória, CGR Brasil News, Band, g1, Conexão Safra, Revista Cafeicultura, Collabstr, Later, Meta (reels de teste).</p>')
p.append(rod(1, T, "Análise de 25/11/2026"))
pags.append(p)

# Páginas 2 e 3: semanas
for i in (0, 2):
    p = [cab('Programação do Instagram · <em>30/11 a 27/12</em>', '13 carrosséis, 14 reels, 1 sorteio ao vivo e stories todos os dias · horários sugeridos para teste')]
    for nome, sub, rows in SEMANAS[i:i+2]:
        p.append(f'<h2>{nome} <span>{sub}</span></h2>')
        p.append(tabela(rows))
    p.append(rod(2 + i // 2, T))
    pags.append(p)

# Página 4: o que mudou + série
p = [cab('O que mudou e <em>por quê</em>', 'Mantivemos o que já tinha boa proposta e reforçamos o que mais viraliza no nicho')]
p.append('''<div class="col"><div>
<div class="box"><h3>Mantido</h3><ul>
<li>Toda a semana de Natal, o sorteio e as datas de venda (kits até 10/12, sorteio em 22/12).</li>
<li>Os reels de bastidor (máquina, provador, saca de R$ 50 mil, torra), que já seguem a lógica de "bastidor nunca visto".</li>
<li>Os carrosséis de lote, ficha sensorial, cafeterias e ceia com harmonizações.</li>
</ul></div><br>
<div class="box"><h3>Novo</h3><ul>
<li><b>Um rosto para a marca:</b> série "Um dia na Fanadinho" aos domingos, com alguém da equipe mostrando a rotina, com humor. É o formato que mais cresceu no café brasileiro.</li>
<li><b>4 reels por semana</b> em vez de 3. Constância conta mais do que perfeição.</li>
<li><b>"Por que café especial custa mais?"</b> (11/12) no lugar do carrossel com fotos de clientes, que contaria contra a regra de originalidade.</li>
<li><b>Esquete "tipos de gente tomando café na ceia"</b> (20/12) e <b>"2026 em 20 segundos"</b> (27/12).</li>
<li><b>Série "Nem todo grão chega até aqui":</b> a máquina (ep. 1) e a torra (ep. 2), para o público voltar.</li>
</ul></div>
</div><div>
<div class="box"><h3>Série "Um dia na Fanadinho" · como gravar</h3><ul>
<li>Escolher <b>uma pessoa fixa</b> da equipe, que goste de câmera e autorize o uso de imagem.</li>
<li>Vídeos de 15 a 30 s, na vertical, falando direto para a câmera, sem roteiro decorado.</li>
<li>Abrir com uma situação: "6h da manhã na Fanadinho e já tem…", "O que ninguém te conta sobre…".</li>
<li>Uma cena engraçada ou inesperada por episódio. Pode ter tropeço, cachorro e chuva: é o real que prende.</li>
<li>Fechar sempre com a mesma frase, para virar marca registrada.</li>
<li>Foco no processo e no cuidado com o café, sem contar a história de pai e avô (regra da marca).</li>
</ul></div><br>
<div class="box"><h3>Pendências</h3><ul>
<li class="pend">Escolher o rosto da marca e gravar o ep. 1 até 05/12.</li>
<li class="pend">Fotos das latas: 30/11, até as 10h.</li>
<li class="pend">Máquina de seleção: gravar sexta, 27/11.</li>
<li class="pend">Foto do kit do sorteio: 02/12.</li>
<li class="pend">Autorização do sorteio no Ministério da Fazenda: confirmar com a contabilidade.</li>
</ul></div>
</div></div>''')
p.append(rod(4, T, "Me mande os vídeos à medida que gravar; eu edito com cortes, textos na tela e os dois ganchos de teste"))
pags.append(p)

# Página 5: sorteio e rotina (mantida da versão anterior)
p = [cab('Sorteio e <em>rotina de cada post</em>', 'O que vale para o mês inteiro')]
p.append('''<div class="col"><div>
<div class="box"><h3>Sorteio do kit do café campeão</h3><ul>
<li><b>Prêmio:</b> caixa, xícara com silk da logo Ornatto e uma lata do Bombom de Licor (F2), campeão do Prêmio Chapada de Minas 2026, categoria Natural. Uma saca dele foi leiloada por R$ 50 mil.</li>
<li><b>Para participar:</b> comprar a partir de R$ 30 de 02 a 21/12, seguir a @ornattocafes e postar o café marcando a @ornattocafes. Quem postar nos stories manda o print no direct.</li>
<li><b>Regras:</b> uma chance por pessoa. Perfil aberto no dia do sorteio. Um ganhador.</li>
<li><b>Sorteio:</b> ao vivo na terça, 22/12, às 19h. O ganhador tem 1 semana para responder. Frete por conta da Ornatto.</li>
<li><b>Stories de 02 a 21/12:</b> repost dos participantes e "faltam X dias".</li>
</ul></div><br>
<div class="box"><h3>Datas que movem a programação</h3><ul>
<li><b>Até 10/12:</b> pedidos de latas e kits de Natal (Flor de Laranjeira R$ 79,90 / kit R$ 109,90 · Mel do Engenho R$ 59,90 / kit R$ 89,90).</li>
<li><b>14 a 18/12:</b> rota do Alex por cafeterias.</li>
<li><b>14 a 23/12:</b> entregas de Natal.</li>
<li><b>24 e 25/12:</b> recesso. Posts e stories ficam agendados.</li>
</ul></div>
</div><div>
<div class="box"><h3>Rotina de cada post</h3><ul>
<li>Reels ★: publicar primeiro como <b>reel de teste</b> (só para quem não segue), com o gancho A e, em outro, o B. Depois de 24 h, o que tiver mais alcance vai para os seguidores.</li>
<li>Terminar pedindo um <b>envio</b> ("manda para quem…"), além do salvamento.</li>
<li>Compartilhar nos stories até 30 minutos depois de publicar.</li>
<li>Responder todos os comentários na primeira hora.</li>
<li>Usar áudio em alta só quando combinar com a marca. Identidade vale mais que tendência.</li>
<li>Toda segunda-feira, anotar alcance de quem não segue, envios, salvamentos, cliques no link e mensagens no WhatsApp de cada post.</li>
</ul></div>
</div></div>''')
p.append(rod(5, T, "Versão de 25/11/2026"))
pags.append(p)

body = "\n".join(f'<section class="pagina">\n' + "\n".join(p) + "\n</section>" for p in pags)
out = f'<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<title>Programação Instagram · Ornatto</title>\n<style>{css}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n'
(AQUI / "programacao.html").write_text(out)
print("ok", len(pags), "páginas")
