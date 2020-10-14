from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Contato
from django.core.paginator import Paginator
# o Q é para fazer consultas com query mais elaboradas
from django.db.models import Q, Value
from django.db.models.functions import Concat


def index(request):
    # contatos = Contato.objects.all()
    # Ordenar os contatos pelo id de forma descrescente e o filtro serve para exibir
    # só os valores com a variavel mostrar verdadeira
    contatos = Contato.objects.order_by('-id').filter(
        mostrar=True
    )

    paginator = Paginator(contatos, 5)
    page = request.GET.get('page')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos': contatos,
    })


def ver_contato(request, contato_id):
    # try:
    #     contato = Contato.objects.get(id=contato_id)
    #     return render(request, 'contatos/ver_contato.html', {
    #         'contato': contato,
    #     })
    # except Contato.DoesNotExist as e:
    #     raise Http404()
    # contato = Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato, id=contato_id)
    if not contato.mostrar:
        raise Http404()

    return render(request, 'contatos/ver_contato.html', {
        'contato': contato,
    })


def busca(request):
    termo = request.GET.get('termo')
    # print(termo)

    # A busca abaixo estava funcionando, mais não buscava por nome
    # e sobrenome ao mesmo tempo, pois não havia um campo onde o nome e sobrenome estivessem juntos
    # contatos = Contato.objects.order_by('-id').filter(
    #     # #    o __icontains vai procurar por um nome que contenha parte do termo, como o like no sql
    #     #     nome__icontains = termo,

    #     # o Pip |(barra) significa OU(OR)
    #     Q(nome__icontains=termo) | Q(sobrenome__icontains=termo),
    #     mostrar=True
    # )

    if termo is None:
        raise Http404()
    campos = Concat('nome', Value(' '), 'sobrenome')

    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo)
    )
    print(contatos.query)

    paginator = Paginator(contatos, 5)
    page = request.GET.get('page')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/busca.html', {
        'contatos': contatos,
    })
