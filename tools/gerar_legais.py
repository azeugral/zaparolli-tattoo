"""Gera privacidade.html e termos.html com o cabeçalho e o rodapé da página do portfólio.
Os textos ficam aqui; atualizar a data de VIGENCIA quando mudar algo.
Uso: python tools/gerar_legais.py"""
import os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
VIGENCIA = '24 de outubro de 2026'
ZAP = '(48) 99810-0176'
ZAP_LINK = 'https://wa.me/5548998100176'

PRIVACIDADE = f'''
<p class="vigencia">Em vigor desde {VIGENCIA}</p>
<p class="abre">Esta política explica, em linguagem direta, quais dados pessoais passam por este site, para que servem e quais são os seus direitos, de acordo com a Lei Geral de Proteção de Dados Pessoais (Lei nº 13.709/2018, LGPD).</p>

<h2>1. Quem é o responsável</h2>
<p>O responsável pelos dados (controlador) é <strong>Thiago Zaparolli</strong>, tatuador que atende como <strong>Zaparolli Tattoo</strong>, em estúdio privado em São José, Santa Catarina. Ele também é o encarregado pelo tratamento de dados. Para qualquer assunto sobre seus dados, fale pelo WhatsApp <a href="{ZAP_LINK}" target="_blank" rel="noopener">{ZAP}</a>.</p>

<h2>2. O que o site coleta</h2>
<p><strong>O site não tem cadastro, não tem área de login e não guarda o que você digita.</strong> O formulário de orçamento apenas monta uma mensagem no seu aparelho e abre o WhatsApp com ela pronta. Nada é enviado a um servidor nosso: a mensagem só chega ao estúdio se você decidir enviá-la pelo WhatsApp.</p>
<p>Na conversa pelo WhatsApp, você pode compartilhar:</p>
<ul>
  <li>nome, cidade e número de telefone (este último já é visível no próprio WhatsApp);</li>
  <li>a ideia da tatuagem, o local do corpo, o tamanho e o estilo;</li>
  <li>fotos de referência, fotos do local a ser tatuado e, no caso de coberturas, fotos da tatuagem antiga.</li>
</ul>
<p>Fotos do corpo podem revelar características sensíveis. Envie apenas o necessário para o orçamento.</p>

<h2>3. Para que usamos</h2>
<ul>
  <li>Responder o seu contato e fazer o orçamento (procedimentos preliminares a um contrato, art. 7º, V, da LGPD).</li>
  <li>Agendar, preparar o desenho e realizar a sessão, e orientar os cuidados depois dela (execução de contrato).</li>
  <li>Cumprir obrigações legais e sanitárias aplicáveis ao estúdio (art. 7º, II).</li>
  <li>Publicar fotos do trabalho nas redes e no portfólio <strong>somente com a sua autorização</strong> (consentimento, art. 7º, I), que pode ser retirada a qualquer momento.</li>
</ul>
<p>Os dados não são vendidos nem usados para propaganda de terceiros.</p>

<h2>4. Com quem os dados podem ser compartilhados</h2>
<ul>
  <li><strong>WhatsApp (Meta)</strong>, quando você conversa com o estúdio. O WhatsApp tem a própria política de privacidade.</li>
  <li><strong>GitHub Pages (GitHub, Inc.)</strong>, que hospeda este site. Como qualquer servidor, ele registra dados técnicos de acesso, como o endereço IP, para segurança e funcionamento.</li>
  <li>Autoridades públicas, quando houver obrigação legal ou ordem judicial.</li>
</ul>
<p>Alguns desses serviços podem processar dados fora do Brasil, com as garantias previstas na LGPD.</p>

<h2>5. Cookies e armazenamento no navegador</h2>
<p>Este site <strong>não usa cookies de rastreamento, de publicidade nem de estatísticas</strong>. As fontes e as imagens são servidas pelo próprio site, sem chamadas a serviços de terceiros ao abrir a página.</p>
<p>A única informação guardada no seu navegador é a sua escolha no aviso de cookies (armazenamento local, chamado <em>localStorage</em>), para o aviso não aparecer em toda visita. Você pode rever essa escolha pelo link <a href="#" data-preferencias>Preferências de cookies</a>, no rodapé, ou apagar os dados do site nas configurações do navegador.</p>
<p>Se no futuro o site passar a usar alguma ferramenta de estatística, ela só será ativada com o seu aceite, e esta política será atualizada antes.</p>
<p>Ao clicar em links para o WhatsApp ou o Instagram, você sai deste site e passa a seguir as regras desses serviços.</p>

<h2>6. Por quanto tempo guardamos</h2>
<p>As conversas e fotos de orçamento ficam no WhatsApp do estúdio pelo tempo necessário para o atendimento, os retoques e eventuais garantias, e depois podem ser apagadas a seu pedido. Registros exigidos por lei são mantidos pelo prazo legal.</p>

<h2>7. Seus direitos</h2>
<p>Você pode, a qualquer momento e sem custo, pedir:</p>
<ul>
  <li>confirmação de que tratamos seus dados e acesso a eles;</li>
  <li>correção de dados incompletos ou desatualizados;</li>
  <li>apagamento de dados desnecessários ou tratados com base no seu consentimento;</li>
  <li>retirada da autorização para publicar fotos do seu trabalho;</li>
  <li>informação sobre com quem os dados foram compartilhados.</li>
</ul>
<p>Basta pedir pelo WhatsApp <a href="{ZAP_LINK}" target="_blank" rel="noopener">{ZAP}</a>. Se achar que seu pedido não foi atendido, você também pode procurar a Autoridade Nacional de Proteção de Dados (ANPD).</p>

<h2>8. Segurança</h2>
<p>O site funciona com conexão segura (HTTPS) e não armazena dados pessoais. As conversas acontecem em um aplicativo com criptografia de ponta a ponta. Ainda assim, nenhum meio digital é totalmente livre de riscos.</p>

<h2>9. Menores de idade</h2>
<p>O site não é direcionado a menores de 18 anos. O atendimento a menores segue a legislação vigente e é tratado diretamente no orçamento.</p>

<h2>10. Mudanças nesta política</h2>
<p>Esta política pode ser atualizada. A data no topo mostra a versão em vigor.</p>
'''

TERMOS = f'''
<p class="vigencia">Em vigor desde {VIGENCIA}</p>
<p class="abre">Estes termos valem para o uso deste site. Ao navegar por ele, você concorda com as condições abaixo.</p>

<h2>1. Sobre o site</h2>
<p>Este é o site de apresentação de <strong>Thiago Zaparolli</strong> (Zaparolli Tattoo), tatuador com estúdio privado em São José, Santa Catarina. Ele mostra o portfólio, explica como funciona o atendimento e facilita o pedido de orçamento pelo WhatsApp.</p>

<h2>2. Orçamentos e agendamentos</h2>
<ul>
  <li>Enviar um pedido pelo site ou pelo WhatsApp <strong>não garante uma data</strong> nem gera obrigação para nenhuma das partes.</li>
  <li>Valores, prazos, número de sessões e condições de agendamento são combinados diretamente com o estúdio, caso a caso, depois da análise da ideia, do local do corpo e, nas coberturas, da tatuagem antiga.</li>
  <li>As informações do site têm caráter informativo e podem mudar sem aviso. Vale sempre o que for combinado na conversa com o estúdio.</li>
  <li>O resultado de uma tatuagem depende também da pele, da cicatrização e dos cuidados de cada pessoa. Fotos do portfólio mostram trabalhos já feitos e não são promessa de resultado idêntico.</li>
</ul>

<h2>3. Sinal, remarcação e cancelamento</h2>
<ul>
  <li>A reserva de uma data pode exigir o pagamento de um sinal. O valor, o prazo e as regras de remarcação e cancelamento são informados <strong>antes</strong> de qualquer pagamento, e só valem depois que você concorda com eles.</li>
  <li>Pedidos de remarcação devem ser feitos com antecedência, pelo WhatsApp, para que o horário possa ser oferecido a outra pessoa.</li>
  <li>Os seus direitos como consumidor, previstos no Código de Defesa do Consumidor, são sempre respeitados.</li>
</ul>

<h2>4. Saúde e cuidados</h2>
<ul>
  <li>Informe ao tatuador, antes da sessão, condições de saúde, alergias, uso de medicamentos, gravidez ou qualquer situação que possa interferir no procedimento.</li>
  <li>O estúdio segue as normas sanitárias aplicáveis, com material descartável e esterilização adequada.</li>
  <li>Os cuidados depois da sessão são passados pelo tatuador e são essenciais para uma boa cicatrização.</li>
</ul>

<h2>5. Direitos autorais</h2>
<p>Todas as artes, desenhos, fotos, textos e a marca Zaparolli exibidos no site são de autoria de Thiago Zaparolli ou usados com autorização, e são protegidos pela Lei de Direitos Autorais (Lei nº 9.610/1998). Não é permitido copiar, reproduzir, tatuar, revender ou usar esse material, total ou parcialmente, sem autorização por escrito. Os projetos são autorais e feitos sob medida para cada cliente.</p>
<p>Fotos de clientes só aparecem com autorização deles. Se você aparece em alguma foto e quer que ela saia, peça pelo WhatsApp e ela será retirada.</p>

<h2>6. Uso adequado</h2>
<p>Ao usar o site, você se compromete a não tentar prejudicar o seu funcionamento, não usar o conteúdo para fins ilegais e não se passar por outra pessoa nos contatos com o estúdio.</p>

<h2>7. Links para outros serviços</h2>
<p>O site tem links para o WhatsApp e o Instagram. Esses serviços têm termos e políticas próprios, que não são controlados pelo estúdio.</p>

<h2>8. Responsabilidade</h2>
<p>O estúdio se esforça para manter o site correto e no ar, mas não garante que ele esteja livre de erros ou sempre disponível. O site não substitui a conversa com o tatuador, especialmente sobre saúde, cuidados e contraindicações.</p>

<h2>9. Privacidade</h2>
<p>O tratamento de dados pessoais está descrito na <a href="privacidade.html">Política de Privacidade</a>.</p>

<h2>10. Lei e foro</h2>
<p>Estes termos seguem as leis do Brasil, incluindo o Código de Defesa do Consumidor. Fica eleito o foro do domicílio do consumidor para resolver eventuais conflitos.</p>

<h2>11. Contato</h2>
<p>Dúvidas sobre estes termos: WhatsApp <a href="{ZAP_LINK}" target="_blank" rel="noopener">{ZAP}</a>.</p>
'''

PAGINAS = {
    'privacidade.html': ('Política de Privacidade', 'Privacidade', 'Como o site da Zaparolli Tattoo trata dados pessoais, cookies e os seus direitos pela LGPD.', PRIVACIDADE),
    'termos.html': ('Termos de Uso', 'Termos', 'Condições de uso do site da Zaparolli Tattoo: orçamentos, direitos autorais e responsabilidades.', TERMOS),
}


def main():
    base = open(os.path.join(SITE, 'portfolio.html'), encoding='utf-8').read()
    cab = base[:base.index('<main>')]
    pe = base[base.index('</main>') + len('</main>'):]
    pe = re.sub(r'\n<div class="luz".*?</div>\n</div>\n', '\n', pe, flags=re.S)
    pe = pe.replace('<script src="assets/js/obras.js"></script>\n', '')
    for arq, (titulo, chapeu, desc, corpo) in PAGINAS.items():
        h = cab
        h = re.sub(r'<title>.*?</title>', f'<title>{titulo} · Zaparolli Tattoo</title>', h)
        h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h)
        h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{titulo} · Zaparolli Tattoo">', h)
        h = h.replace('portfolio.html">', arq + '">')
        html = h + f'''<main>
  <section class="secao pagina-topo legal">
    <div class="wrap">
      <p class="chapeu">{chapeu}</p>
      <h1 class="titulo"><span class="desgaste">{titulo}</span></h1>
      <div class="legal-corpo">{corpo}</div>
    </div>
  </section>
</main>''' + pe
        open(os.path.join(SITE, arq), 'w', encoding='utf-8').write(html)
        print(arq)


if __name__ == '__main__':
    main()
