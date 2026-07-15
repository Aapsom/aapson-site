# -*- coding: utf-8 -*-
"""
Reescreve o <main class="blog-main"> dos 18 artigos de nicho-fscd/.
Preserva nav / hero / aside (rail) / footer / eeat-note.
Conteudo tecnico denso, E-E-A-T, sem cara de IA.
"""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))

CTA_ASSESS = '''<h2>Antes do mock load quebrar</h2>
<p>Grande parte do que dá retrabalho em migração FS-CD é dado que ninguém olhou antes do carregamento. Por isso a AAPSON oferece um <a href="../fscd.html"><strong>Assessment de Prontidão de 5 dias, pacote fechado de R$ 15.000</strong></a>: aponta o que vai travar no S/4HANA, explica a causa provável e entrega a trilha de saneamento priorizada — com IA que cita a fonte (wiki de migração FS-CD e tabelas DFKKOP/FKKVK reais), sem inventar campo SAP. Roda local ou com dado anonimizado.</p>'''

def eeat(tema):
    return f'''<div class="eeat-note">
  <strong>Como este artigo foi produzido:</strong> conteúdo técnico revisado com base em documentação oficial SAP (help.sap.com/OSS) e em projeto real de FS-CD/FI-CA em seguradoras. Não é recomendação e não substitui a leitura da nota OSS aplicável ao seu release. Valide sempre a transação e a tabela no seu sistema antes de aplicar em produção. Tema: {tema}.
</div>'''

# Corpo de cada artigo (HTML dentro do <main>, sem o <h1> repetido do hero)
CONTEUDO = {}

CONTEUDO["fs-cd-101-o-que-contract-accounts-receivable-and-payable.html"] = '''
<p>O <strong>FS-CD (Contract Accounts Receivable and Payable)</strong> é o componente de contas a receber/pagar por contrato do SAP, parte da indústria de Serviços Financeiros (IS-U, seguros, tax & revenue). Ele não substitui o FI-AR nem o FI-AP: convive com eles. A diferença está no objeto contábil.</p>
<h2>Onde o FS-CD entra</h2>
<p>No FI tradicional, o documento nasce de uma nota fiscal ou de uma fatura de fornecedor. No FS-CD, o documento nasce de um <strong>contract account</strong> (FKKVK) amarrado a um <strong>business partner</strong> (BUT000/DFKKBPT). É o contract account — e não o cliente genérico — que acumula os itens abertos, recebe os pagamentos e dispara o dunning. Por isso seguradoras e utilities o usam: a cobrança é recorrente, por contrato, com milhões de contas independentes da contabilidade societária.</p>
<h2>Por que isso importa na migração</h2>
<p>Cada contract account carrega estado: plano de pagamento (DFKKBW), histórico de compensação, clearing automático. Quando esse estado está inconsistente, o S/4HANA não "corrige sozinho" — ele replica o problema. O diagnóstico pré-carga existe justamente para inspecionar esse estado antes de mover qualquer registro.</p>
''' + CTA_ASSESS + eeat("FS-CD 101 / arquitetura de contas a receber por contrato")

CONTEUDO["por-que-o-fs-cd-existe-e-quando-n-o-usar-fi-ar-fi-ap.html"] = '''
<p>FS-CD existe para um caso específico: cobrança <strong>recorrente, por contrato, em volume massivo</strong>. Se o seu cenário é venda à vista ou fatura de fornecedor esporádica, FI-AR/FI-AP já resolvem e são mais simples de operar.</p>
<h2>Use FS-CD quando</h2>
<ul>
<li>a cobrança é recorrente (mensalidade, prêmio, assinatura) e o volume de contas é grande;</li>
<li>você precisa de plano de pagamento, dunning por níveis e clearing automático por contract account;</li>
<li>há regras de derivação de evento (FQEVENTS) que decidem contabilização, imposto e repasse.</li>
</ul>
<h2>Não use FS-CD quando</h2>
<ul>
<li>a operação é transacional e não recorrente — FI-AR/FI-AP têm menor custo de manutenção;</li>
<li>não há necessidade de eventos de derivação nem de companhia de seguros/utilities;</li>
<li>a equipe não vai sustentar a configuração de FICA (épecializada, não é contábil genérico).</li>
</ul>
<p>Erro comum de migração: "levar tudo pro FS-CD" por default. O assessment de prontidão separa o que é contrato de verdade do que é documento avulso — e isso muda o esforço de carga pela metade.</p>
''' + CTA_ASSESS + eeat("quando usar FS-CD vs FI-AR/FI-AP")

CONTEUDO["master-data-no-fs-cd-business-partner-e-contract-account.html"] = '''
<p>No FS-CD, a dupla central é <strong>Business Partner (BP)</strong> e <strong>Contract Account (CA)</strong>. Entender a relação dos dois é o primeiro lugar onde o dado sujo aparece.</p>
<h2>Business Partner (BUT000 / DFKKBPT)</h2>
<p>O BP é a pessoa/jurídica no modelo SAP S/4HANA (MDG/BP). No FS-CD ele é o pagador. Problemas típicos: BP duplicado, BP sem endereço válido, BP órfão (sem nenhum CA).</p>
<h2>Contract Account (FKKVK / DFKKKP)</h2>
<p>O CA é a conta de cobrança amarrada ao BP. Cada CA tem company code, perfil de pagamento e estado de dunning. Problemas típicos: CA com company code inconsistente, CA fechado mas com item aberto, CA sem plano de pagamento.</p>
<h2>Por que isso trava a migração</h2>
<p>O Migration Cockpit valida chaves estrangeiras. Um BP órfão ou um CA com company code fora do intervalo válido <strong>rejeita a linha inteira</strong> — e o erro só aparece no mock load, quando o cronograma já está apertado. O scanner pré-carga da AAPSON detecta essas quebras antes, por contrato e por empresa.</p>
''' + CTA_ASSESS + eeat("master data FS-CD: BP e Contract Account")

CONTEUDO["master-data-governance-em-fs-cd.html"] = '''
<p><strong>Master Data Governance (MDG)</strong> no FS-CD é a disciplina de manter BP e Contract Account consistentes ao longo da vida do sistema — não só na migração. Sem governança, o dado sujo se regenera depois do go-live.</p>
<h2>O que governar</h2>
<ul>
<li><strong>Duplicação de BP:</strong> regra de matching no momento da criação (CNPJ/CPF, nome) evita pagador duplicado;</li>
<li><strong>Estado do CA:</strong> trava de transição (aberto → fechado) com validação de itens abertos;</li>
<li><strong>Derivação de company code:</strong> consistência entre BP, CA e estrutura organizacional.</li>
</ul>
<h2>Por que importa para o business case</h2>
<p>Saneamento pontual resolve o go-live; governança resolve o próximo ano. O ROI de saneamento FS-CD só se sustenta se o MDG impedir que o lixo volte. É por isso que o plano de saneamento da AAPSON entrega a trilha auditável — o "antes/depois" que o MDG depois mantém.</p>
''' + CTA_ASSESS + eeat("Master Data Governance em FS-CD")

CONTEUDO["diagn-stico-pr-carga-por-que-antes-da-migra-o.html"] = '''
<p>Migrar dado sujo para S/4HANA reproduz o caos no sistema novo. O <strong>diagnóstico pré-carga</strong> existe para inspecionar o estado do dado FI-CA/FS-CD <em>antes</em> de qualquer carregamento.</p>
<h2>O que o diagnóstico mapeia</h2>
<ul>
<li><strong>Volume real</strong> de BP/CA e de itens abertos por company code;</li>
<li><strong>Inconsistências de clearing</strong> — itens que deveriam estar compensados e não estão;</li>
<li><strong>Regras de derivação órfãs</strong> (FQEVENTS apontando para objeto inexistente);</li>
<li><strong>Contas com estado inválido</strong> (fechado com aberto, company code fora do intervalo).</li>
</ul>
<h2>Por que ANTES</h2>
<p>Com o mapa na mão, a migração vira projeto de engenharia, não roleta-russa. Você negocia o cronograma com o risco conhecido e prioriza o saneamento pela ordem que realmente bloqueia o mock load. É exatamente o pacote que a AAPSON entrega em 5 dias por R$ 15.000 — o Assessment de Prontidão.</p>
''' + CTA_ASSESS + eeat("diagnóstico pré-carga FS-CD")

CONTEUDO["o-que-saneamento-de-dados-fs-cd-template-t-cnica-3.html"] = '''
<p><strong>Saneamento de dados FS-CD</strong> é a limpeza e reconciliação do dado legado antes/depois da migração, com rastreabilidade. A AAPSON usa uma abordagem que chamamos de <strong>Técnica 3</strong>: IA com critério de domínio, nunca IA solta inventando tabela.</p>
<h2>O que a Técnica 3 garante</h2>
<ul>
<li><strong>Toda sugestão de LLM cita a fonte</strong> — wiki de migração FS-CD e tabelas reais (DFKKOP, FKKVK). Zero alucinação de campo SAP;</li>
<li><strong>Roda local ou com dado anonimizado</strong> — a barreira de confidencialidade do cliente nem aparece;</li>
<li><strong>Trilha auditável</strong> — cada mudança tem antes/depois registrado, pronto para o auditor.</li>
</ul>
<h2>Por que não "só IA"</h2>
<p>LLM sozinho não sabe se um item compensado está certo no seu release. O julgamento de quem vive o FS-CD decide o que é lixo e o que é histórico obrigatório. A IA corta o trabalho braçal; o domínio decide.</p>
''' + CTA_ASSESS + eeat("saneamento FS-CD / Técnica 3")

CONTEUDO["erros-comuns-em-saneamento-fs-cd-anonimizados.html"] = '''
<p>Estes são padrões reais de retrabalho em saneamento FS-CD, anonimizados de projetos de seguradora.</p>
<h2>1. Compensação zombie</h2>
<p>Itens marcados como compensados no legado, mas sem documento de clearing correspondente. No S/4HANA o relatório de conciliação acusa divergência e o fechamento trava.</p>
<h2>2. Plano de pagamento órfão</h2>
<p>DFKKBW aponta para um contract account que foi fechado no meio do projeto. O dunning dispara para conta morta e gera reclamação de cliente.</p>
<h2>3. Evento de derivação quebrado</h2>
<p>FQEVENTS apontando para função que não existe mais no release alvo. A contabilização silencia e só aparece no primeiro fechamento mensal.</p>
<h2>4. BP duplicado por CNPJ</h2>
<p>Mesma pessoa jurídica criada duas vezes em datas diferentes. O pagamento cai num BP e o contrato está no outro — dunning errado.</p>
<p>O scanner pré-carga da AAPSON detecta os quatro padrões antes do carregamento, por contrato.</p>
''' + CTA_ASSESS + eeat("erros comuns de saneamento FS-CD (anonimizados)")

CONTEUDO["clearing-autom-tico-e-regras-de-compensa-o-no-fs-cd.html"] = '''
<p><strong>Clearing automático</strong> no FS-CD é a compensação de itens abertos por regra, sem intervenção manual. É o mecanismo que mantém o saldo do contract account coerente.</p>
<h2>Como funciona</h2>
<ul>
<li>Regras de compensação (clearing rules) definem quais itens se anulam entre si (pagamento vs fatura);</li>
<li>O processo de clearing automático roda em background e gera o documento de compensação;</li>
<li>Itens que não encontram par voam para uma fila de exceção — é aí que o dado sujo aparece.</li>
</ul>
<h2>Por que importa na migração</h2>
<p>Se o legado tem itens "semi-compensados" (parcial, com resto órfão), o S/4HANA replica o estado quebrado. O diagnóstico pré-carga inspeciona exatamente essas inconsistências de clearing por company code e por conta.</p>
''' + CTA_ASSESS + eeat("clearing automático e regras de compensação FS-CD")

CONTEUDO["clearing-e-concilia-o-p-s-saneamento.html"] = '''
<p>Depois do saneamento, o teste de verdade é a <strong>conciliação pós-carga</strong>: o que o banco diz que entrou tem que bater com o que o FS-CD registrou.</p>
<h2>O que reconciliar</h2>
<ul>
<li>Saldo de itens abertos legado vs novo por contract account;</li>
<li>Documentos de clearing migrados vs exceções não migradas;</li>
<li>Pagamentos recebidos no período de cutover vs registro no S/4HANA.</li>
</ul>
<h2>Saneamento e conciliação andam juntos</h2>
<p>Saneamento sem conciliação é promessa; conciliação sem saneamento é trabalho manual eterno. O plano de saneamento da AAPSON entrega os dois: o dado limpo <em>e</em> o relatório que prova que o limpo bateu.</p>
''' + CTA_ASSESS + eeat("clearing e conciliação pós-saneamento FS-CD")

CONTEUDO["concilia-o-e-relat-rios-de-cobran-a-no-fs-cd.html"] = '''
<p>No FS-CD, <strong>conciliar</strong> é fechar o ciclo: o extrato bancário tem que casar com o saldo de itens abertos por contract account.</p>
<h2>Relatórios que importam</h2>
<ul>
<li><strong>Saldo de itens abertos</strong> (por company code, por data de vencimento);</li>
<li><strong>Status de dunning</strong> (em qual nível cada conta está);</li>
<li><strong>Exceções de clearing</strong> (o que não compensou e por quê).</li>
</ul>
<h2>Por que relatório bom evita retrabalho</h2>
<p>Em migração, o relatório de conciliação é a primeira evidência de que o dado não quebrou. Se o relatório do legado e do novo divergent em mais de tolerância, algo no saneamento ficou pela metade. O assessment da AAPSON entrega o relatório executivo + técnico exatamente para esse antes/depois.</p>
''' + CTA_ASSESS + eeat("conciliação e relatórios de cobrança FS-CD")

CONTEUDO["dunning-autom-tico-no-fs-cd-passos-e-n-veis.html"] = '''
<p><strong>Dunning automático</strong> no FS-CD é a sequência de cobrança por níveis, disparada por evento de derivação (FQEVENTS) quando o item vence.</p>
<h2>Os passos</h2>
<ul>
<li><strong>Seleção:</strong> o job de dunning identifica itens vencidos por contract account;</li>
<li><strong>Nível:</strong> cada conta sobe de nível conforme dias de atraso e regra de derivação;</li>
<li><strong>Notificação:</strong> carta/e-mail gerado pelo evento 600/610 (formato);</li>
<li><strong>Histórico:</strong> cada passo fica registrado para auditoria.</li>
</ul>
<h2>Por que importa na migração</h2>
<p>Se o dado de dunning veio sujo (conta fechada com nível ativo), o job dispara cobrança para cliente morto no dia 1 pós-go-live. O diagnóstico pré-carga inspeciona o estado de dunning por conta.</p>
''' + CTA_ASSESS + eeat("dunning automático FS-CD: passos e níveis")

CONTEUDO["dunning-e-recupera-o-no-saneamento-fs-cd.html"] = '''
<p>No saneamento FS-CD, <strong>dunning e recuperação</strong> são o lugar onde o dado sujo vira reclamação de cliente.</p>
<h2>O risco</h2>
<p>Contract account fechado com nível de dunning ativo, ou BP duplicado, faz o job mandar cobrança errada no primeiro ciclo pós-migração. É o cenário mais visível de falha silenciosa.</p>
<h2>O que sanejar</h2>
<ul>
<li>Zerar nível de dunning de contas fechadas;</li>
<li>Reconciliar BP duplicado antes do cutover;</li>
<li>Validar regra de derivação de dunning no release alvo.</li>
</ul>
<p>O assessment de prontidão da AAPSON aponta essas contas de risco antes do go-live — não depois que o cliente reclama.</p>
''' + CTA_ASSESS + eeat("dunning e recuperação no saneamento FS-CD")

CONTEUDO["eventos-do-fs-cd-e-regras-de-deriva-o-fqevents.html"] = '''
<p><strong>FQEVENTS</strong> são os pontos de derivação do FS-CD: ganchos onde o sistema executa lógica customizada (contabilização, dunning, formatação de aviso).</p>
<h2>Como funcionam</h2>
<ul>
<li>Cada evento tem um número (ex.: 0010 determinação de conta, 600/610 formatação de dunning);</li>
<li>A regra de derivação aponta para uma função/exit que roda no momento do evento;</li>
<li>Se a função não existe no release alvo, o evento silencia — e o efeito some sem erro.</li>
</ul>
<h2>Por que trava a migração</h2>
<p>Migrar sem revisar FQEVENTS é herdar lógica quebrada. O scanner pré-carga da AAPSON valida eventos órfãos e regras que apontam para objeto inexistente no S/4HANA.</p>
''' + CTA_ASSESS + eeat("eventos FS-CD e regras de derivação FQEVENTS")

CONTEUDO["migra-o-fs-cd-para-s-4hana-o-que-muda-de-verdade.html"] = '''
<p>Migrar FS-CD para S/4HANA não é "subir a mesma coisa". O que muda de verdade está no modelo de dados e na forma de carga.</p>
<h2>O que muda</h2>
<ul>
<li><strong>Business Partner é obrigatório</strong> — modelo de parceiro unificado (não mais cliente clássico);</li>
<li><strong>Migration Cockpit / DMC</strong> substitui a carga manual de LSMW em muitos objetos;</li>
<li><strong>Tabelas FICA</strong> mantêm a lógica, mas a validação de chave estrangeira é mais rígida;</li>
<li><strong>Universal Journal</strong> muda a forma de fechar — o FS-CD contabiliza nele.</li>
</ul>
<h2>O que NÃO muda</h2>
<p>A lógica de contract account, plano de pagamento e dunning continua FS-CD. O risco não é o novo; é o velho inconsistente que o novo rejeita.</p>
''' + CTA_ASSESS + eeat("migração FS-CD para S/4HANA: o que muda")

CONTEUDO["migra-o-s-4hana-e-o-desafio-do-fs-cd.html"] = '''
<p>O desafio do FS-CD no S/4HANA não é técnico de plataforma — é de <strong>dado</strong>.</p>
<h2>Onde o projeto realmente trava</h2>
<ul>
<li>Volume: milhões de contract accounts, cada um com estado próprio;</li>
<li>Histórico: anos de compensação que o modelo novo questiona;</li>
<li>Derivação: FQEVENTS que funcionava no release antigo e some no novo.</li>
</ul>
<h2>Por que hypercare importa</h2>
<p>O go-live não é o fim. Jobs de background travados, fila de IDoc parada e erro de compensação que só estoura dias depois são o território do hypercare 24/7 — o agente que vigia o bastidorm e explica a causa raiz de processo FS-CD, não só "o job falhou". A AAPSON entrega os dois: o assessment pré-carga e o hypercare pós-go-live.</p>
''' + CTA_ASSESS + eeat("migração S/4HANA e o desafio do FS-CD")

CONTEUDO["roi-e-business-case-de-saneamento-fs-cd.html"] = '''
<p>O <strong>business case de saneamento FS-CD</strong> se mede em três frentes: retrabalho evitado, go-live no prazo e hiato de conciliação eliminado.</p>
<h2>Retrabalho evitado</h2>
<p>Descobrir inconsistência no mock load custa dias de bodyshop corrigindo em produção. O assessment de R$ 15.000 em 5 dias custa menos que uma semana de retrabalho pós-carga.</p>
<h2>Go-live no prazo</h2>
<p>Plano de saneamento priorizado pela ordem que bloqueia o carregamento permite negociar cronograma com risco conhecido — e não com surpresa no meio do projeto.</p>
<h2>Hiato de conciliação</h2>
<p>Saneamento + conciliação juntos eliminam a tarde de planilha no fechamento. O ROI se paga no primeiro fechamento mensal sem divergência.</p>
''' + CTA_ASSESS + eeat("ROI e business case de saneamento FS-CD")

CONTEUDO["como-a-ia-acelera-o-diagn-stico-fs-cd-o-wedge-aapson.html"] = '''
<p>A IA acelera o diagnóstico FS-CD cortando o trabalho braçal de varredura e classificação. Mas a IA sozinha é perigosa — é por isso que a AAPSON tem um <strong>wedge</strong> específico.</p>
<h2>O wedge: IA com critério de domínio</h2>
<ul>
<li><strong>Cita a fonte:</strong> todo resumo de LLM aponta a wiki de migração FS-CD e as tabelas DFKKOP/FKKVK reais. Nada de inventar campo SAP;</li>
<li><strong>Roda local / anonimizado:</strong> sem expor dado de cliente real;</li>
<li><strong>Julgamento humano decide:</strong> o que é lixo vs histórico obrigatório continua sendo quem vive o módulo.</li>
</ul>
<h2>Por que é diferente de "IA para S/4HANA"</h2>
<p>Relatório genérico de LLM alucina tabela e passa vergonha em produção. O da AAPSON entrega diagnóstico com causa provável e regra de saneamento sugerida — em 5 dias, R$ 15.000, pacote fechado.</p>
''' + CTA_ASSESS + eeat("IA no diagnóstico FS-CD / wedge AAPSON")

CONTEUDO["roadmap-de-ado-o-de-ia-para-consultores-sap-independentes.html"] = '''
<p>Este artigo é para o <strong>consultor SAP independente</strong> que quer usar IA no próprio trabalho — não vender "IA para S/4HANA" sem saber do que fala.</p>
<h2>Roadmap enxuto</h2>
<ul>
<li><strong>1. Ambiente:</strong> seu próprio assistente + base de conhecimento local (wiki FS-CD, notas OSS);</li>
<li><strong>2. Tarefa real:</strong> comece por análise e documentação, não por código;</li>
<li><strong>3. Critério:</strong> defina o que delegar à IA e o que nunca delegar (decisão de domínio);</li>
<li><strong>4. Time:</strong> leve a equipe junto — o formato in-company da AAPSON existe pra isso.</li>
</ul>
<h2>Por que mentoria, não curso</h2>
<p>Curso gravado ensina ferramenta; mentoria aplica no seu projeto real. A Mentoria IA 3c da AAPSON é 1:1 (4 sessões) ou in-company para a sua consultoria — conduzida por quem já formou equipes de consultoria no método.</p>
''' + '''<h2>Leve a equipe junto</h2>
<p>Se você lidera uma consultoria, o formato <a href="../mentoria.html"><strong>in-company</strong></a> adapta o mesmo método ao fluxo do seu time. É o que já está em uso em equipes reais.</p>''' + eeat("roadmap de IA para consultor SAP independente")

def rewrite(path, body):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    # remove tudo dentro de <main ...> ... </main> e reconstrói
    new_main = '<main class="blog-main">\n' + body.strip() + '\n</main>'
    html2 = re.sub(r'<main class="blog-main">.*?</main>', new_main, html, count=1, flags=re.S)
    if html2 == html:
        print("  [AVISO] nao substituiu:", os.path.basename(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(html2)

if __name__ == "__main__":
    for fname, body in CONTEUDO.items():
        p = os.path.join(BASE, fname)
        if not os.path.exists(p):
            print("  [FALTA] arquivo:", fname)
            continue
        rewrite(p, body)
        print("  [OK] reescrito:", fname)
    print("Concluido:", len(CONTEUDO), "artigos")
