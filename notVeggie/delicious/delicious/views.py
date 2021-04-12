from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from rest_framework import viewsets
from .models import Prato, Reserva, Evento, Utilizador
from django.contrib.auth.models import User
from .forms import UserForm, LoginForm, RegistoForm, PratoForm, ReservaForm
from .serializers import PratoSerializer, ReservaSerializer, EventoSerializer, UserSerializer


def index(request):
    template = loader.get_template('delicious/login.html')
    registo_form = RegistoForm(request.POST or None)
    login_form = LoginForm(request.POST or None)
    context = {
        'registo_form': registo_form,
        'login_form': login_form,
    }

    if request.method == 'POST':
        if 'btnRegisto' in request.POST:
            if registo_form.is_valid():
                registo_form.save(commit=True)
                return redirect(request, "cliente.html", context)
        if 'btnLogin' in request.POST:
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                return redirect(request, "administrador.html", context)

    return HttpResponse(template.render(context, request))


def base(request):
    if request.user.is_authenticated():
        current_user = request.user
        if request.user.is_staff:
            template = loader.get_template('delicious/administrador.html')
            context = {
                'current_user': current_user.username,
            }
            return HttpResponse(template.render(context, request))
            # return render(request, 'delicious/administrador.html', {'current_user': current_user.username})
        else:
            # lista_reservas = User.objects.filter(reserva__nome_cliente_id=request.user.id)
            lista_reservas = Reserva.objects.filter(nome_cliente=current_user.id)
            return render(request, 'delicious/cliente.html',
                          {'current_user': current_user.username, 'minhas_reservas': lista_reservas})

    if 'login_username' in request.POST:
        print("NOVO LOGIN")
        login_username = request.POST['login_username']
        login_password = request.POST['login_password']
        if login_username:
            print("authenticate")
            user = authenticate(username=login_username, password=login_password)
            if user is not None:
                print("user is not none")
                if user.is_active:
                    login(request, user)
                    current_user = request.user
                    print(current_user.id)
                    if request.user.is_staff:
                        template = loader.get_template('delicious/administrador.html')
                        context = {
                            'current_user': current_user.username,
                        }
                        return HttpResponse(template.render(context, request))
                        # return render(request, 'delicious/administrador.html', {'current_user': current_user.username})
                    else:
                        # lista_reservas = User.objects.filter(reserva__nome_cliente_id=request.user.id)
                        lista_reservas = Reserva.objects.filter(nome_cliente=current_user.id)
                        return render(request, 'delicious/cliente.html',
                                      {'current_user': current_user.username, 'minhas_reservas': lista_reservas})
            else:
                return render(request, 'delicious/base.html', {'erro_login': True, 'open_login_modal': True})

    if 'registo_username' in request.POST:
        print("NOVO REGISTO")
        registo_username = request.POST['registo_username']
        registo_email = request.POST['registo_email']
        registo_password = request.POST['registo_password']
        registo_confirmar_password = request.POST['registo_confirmar_password']
        if registo_username:
            ## Verifica se ja existe um User com o mesmo username
            username_existe = User.objects.filter(username=registo_username)
            print(username_existe)
            if len(username_existe) > 0:
                return render(request, 'delicious/base.html',
                              {'erro_registo_username': True, 'open_signup_modal': True})
            else:
                ## Verifica se as passwords inseridas são iguais
                if registo_password != registo_confirmar_password:
                    return render(request, 'delicious/base.html',
                                  {'erro_registo_password': True, 'open_signup_modal': True})
                else:
                    ## Regista o novo User
                    novo_user = User(username=registo_username, email=registo_email)
                    novo_user.set_password(novo_user.password)
                    novo_user.save()
                    lista_reservas = Reserva.objects.filter(nome_cliente=novo_user.id)
                    return render(request, 'delicious/cliente.html', {'current_user': request.user.username, 'minhas_reservas': lista_reservas})
        else:
            return render(request, 'delicious/base.html', {'erro_registo_username': True, 'open_signup_modal': True})

    template = loader.get_template('delicious/base.html')
    return HttpResponse(template.render({}, request))


def cliente(request):
    print("view cliente")
    if request.user.is_authenticated():
        if not request.user.is_staff:
            current_user = request.user
            return render(request, 'delicious/cliente.html', {'current_user': current_user.username})
        else:
            template = loader.get_template('delicious/erro.html')
            return HttpResponse(template.render({}, request))

    if 'criar_reserva_n_lugares' in request.POST:
        print("NOVA RESERVA!")
        criar_reserva_data = request.POST['criar_reserva_data']
        criar_reserva_hora = request.POST['criar_reserva_hora']
        criar_reserva_n_lugares = request.POST['criar_reserva_n_lugares']
        criar_reserva_contacto = request.POST['criar_reserva_contacto']
        current_user = request.user
        if criar_reserva_data:
            nova_reserva = Reserva(data=criar_reserva_data, hora=criar_reserva_hora,
                                   n_lugares=criar_reserva_n_lugares,
                                   nome_cliente=current_user, contacto=criar_reserva_contacto)
            nova_reserva.save()
            return render(request, 'delicious/cliente.html', {'current_user': current_user.username})
        else:
            print("erro a criar reserva")

    template = loader.get_template('delicious/erro.html')
    return HttpResponse(template.render({}, request))


def administrador(request):
    print("view administrador")
    if request.user.is_authenticated():
        if request.user.is_staff:
            current_user = request.user
            return render(request, 'delicious/administrador.html', {'current_user': current_user.username})
        else:
            template = loader.get_template('delicious/erro.html')
            return HttpResponse(template.render({}, request))
    else:
        template = loader.get_template('delicious/erro.html')
        return HttpResponse(template.render({}, request))


def loginView(request):
    if request.user.is_authenticated():
        current_user = request.user
        return render(request, 'delicious/cliente.html', {'current_user': current_user.id})
    else:
        if 'login_username' in request.POST:
            login_username = request.POST['login_username']
            login_password = request.POST['login_password']
            if login_username:
                print("authenticate")
                user = authenticate(username=login_username, password=login_password)
                if user is not None:
                    print("user is not none")
                    if user.is_active:
                        login(request, user)
                        current_user = request.user
                        print(current_user.id)
                        return render(request, 'delicious/cliente.html', {'current_user': current_user.username})
                else:
                    return render(request, 'delicious/login.html', {'erro': True})
        else:
            return render(request, 'delicious/login.html', {'erro': False})


def registo(request):
    if 'registo_username' in request.POST:
        registo_username = request.POST['registo_username']
        registo_email = request.POST['registo_email']
        registo_password = request.POST['registo_password']
        registo_confirmar_password = request.POST['registo_confirmar_password']
        if registo_username:
            ## Verifica se ja existe um User com o mesmo username
            username_existe = User.objects.filter(username=registo_username)
            print(username_existe)
            if len(username_existe) > 0:
                return render(request, 'delicious/registo.html', {'erro_username': True})
            else:
                ## Verifica se as passwords inseridas são iguais
                if registo_password != registo_confirmar_password:
                    return render(request, 'delicious/registo.html', {'erro_password': True})
                else:
                    ## Regista o novo User
                    novo_user = User(username=registo_username, email=registo_email)
                    novo_user.set_password(novo_user.password)
                    novo_user.save()
                    return render(request, 'delicious/cliente.html', {})
        else:
            return render(request, 'delicious/registo.html', {'erro_username': True})
    else:
        return render(request, 'delicious/registo.html', {'erro_username': False})


def menu(request):
    template = loader.get_template('delicious/cliente.html')
    context = {}
    return HttpResponse(template.render(context, request))


def criarPrato(request):
    if request.user.is_authenticated():
        if request.user.is_staff:
            template = loader.get_template('delicious/criarprato.html')
        else:
            template = loader.get_template('delicious/erro.html')
    else:
        template = loader.get_template('delicious/erro.html')

    context = {
    }

    if 'criar_prato_nome' in request.POST:
        criar_prato_nome = request.POST['criar_prato_nome']
        criar_reserva_preco = request.POST['criar_prato_preco']
        if criar_prato_nome:
            novo_prato = Prato(nome=criar_prato_nome, preco=criar_reserva_preco)
            novo_prato.save()
            return render(request, 'delicious/administrador.html', {'current_user': request.user.username})
        else:
            print("erro a criar reserva")

    return HttpResponse(template.render(context, request))


def criarReserva(request):
    if request.user.is_authenticated():
        if not request.user.is_staff:
            template = loader.get_template('delicious/criarreserva.html')
        else:
            template = loader.get_template('delicious/erro.html')
    else:
        template = loader.get_template('delicious/erro.html')

    context = {
    }

    if 'criar_reserva_n_lugares' in request.POST:
        print("NOVA RESERVA!")
        criar_reserva_data = request.POST['criar_reserva_data']
        criar_reserva_hora = request.POST['criar_reserva_hora']
        criar_reserva_n_lugares = request.POST['criar_reserva_n_lugares']
        criar_reserva_contacto = request.POST['criar_reserva_contacto']
        current_user = request.user
        criar_reserva_cliente = current_user.username
        if criar_reserva_data:
            nova_reserva = Reserva(data=criar_reserva_data, hora=criar_reserva_hora,
                                   n_lugares=criar_reserva_n_lugares,
                                   nome_cliente=current_user, contacto=criar_reserva_contacto)
            nova_reserva.save()
            lista_reservas = Reserva.objects.filter(nome_cliente=request.user.id)
            return render(request, 'delicious/cliente.html', {'current_user': current_user.username, 'minhas_reservas': lista_reservas})
        else:
            print("erro a criar reserva")

    return HttpResponse(template.render(context, request))


class PratoViewSet(viewsets.ModelViewSet):
    queryset = Prato.objects.all()
    serializer_class = PratoSerializer


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer


class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserFormView(View):
    form_class = UserForm
    template_name = 'delicious/base.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # retorna objecto User se credenciais estiverem corretas
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('delicious:base')

        return render(request, self.template_name, {'form': form})
