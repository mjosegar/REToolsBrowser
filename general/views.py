from datetime import date
from django.shortcuts import render, redirect 
from django.urls import reverse
from django.contrib.auth import login, logout as user_logout, authenticate
from .models import Tool_Category, Vendor, Tool, Question, Answer, Survey_user, Category_Answer, User_Answer
from django.contrib.auth.hashers import make_password
import json
import numpy as np

from .models import Category

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        if request.POST['password'] == request.POST['confirm-password']:
            try:
                password = make_password(request.POST['password'])

                vendor = Vendor(email=request.POST['email'], name=request.POST['name'], password=password)
                vendor.save()
                login(request, vendor)
                return redirect('home')
            except:
                return render(request, 'signup.html', {
                    'error' : 'Username already exists'
                })

        return render(request, 'signup.html', {
            'error' : 'Passwords do not match'
        })


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
             return render(request, 'signin.html', {
            'error': 'User or password is incorrect'
        })
        else: 
            login(request, user)
            return redirect('home')

def logout(request):
    user_logout(request)
    return redirect('home')

def mytools(request):
    registered = request.GET.get('registered')
    
    tools = Tool.objects.filter(vendor_id=request.user.id)
    return render(request, 'mytools.html', {
        'tools' : tools,
        'registered' : registered
    })

def tool_new(request):
    if request.method == 'GET':
        error = request.GET.get('error')

        root = request.user.is_superuser
        vendors = None
        if root:
            vendors = Vendor.objects.all()
        return render(request, 'tools-form.html', {
            'root' : root,
            'vendors' : vendors,
            'rootback' : root,
            'error' : error
        })
    else:
        try:
            name=request.POST['name']
            vendor = request.user.id

            if (request.POST.get('vendor')):
                vendor = request.POST['vendor']

            if (Tool.objects.get(name=name, vendor_id=vendor)):
                return redirect(reverse('tool_new') + '?error=1')

        except Tool.DoesNotExist:
            fecha = request.POST['date'].split('-')
            fecha = date(int(fecha[0]), int(fecha[1]), 1)
        
            Tool.objects.create(name=name, version=request.POST['version'], date_version=fecha, vendor_id=vendor)

            if (request.user.is_superuser):
                return redirect(reverse('tools') + '?registered=1')
            else:
                return redirect(reverse('mytools') + '?registered=1')
        

def tools(request):
    registered = request.GET.get('registered')
    deleted = request.GET.get('deleted')

    if registered:
        message = "The tool has been registered successfully."
    elif deleted:
        message = "The tool has been deleted successfully."
    else:
        message = ""

    flag = 1 if registered or deleted else 0

    tools = Tool.objects.all()
    tools = [{
        'id' : tool.id,
        'name' : tool.name,
        'version' : tool.version, 
        'date_version' : tool.date_version,
        'vendor' : Vendor.objects.get(email=tool.vendor).name,
        'contact' : tool.vendor,
        'ready' : tool.ready,
    } for tool in tools]
    return render(request, 'tools.html', {
        'tools' : tools,
        'registered' : registered, 
        'flag' : flag,
        'message' : message
    })

def tool_edit(request, id_tool):
    tool = Tool.objects.get(id=id_tool)

    if request.method == 'GET':
        partes = str(tool.date_version).split("-")[:2]
        date_version = "-".join(partes)
        return render(request, 'tools-form.html', {
            'name' : tool.name,
            'version' : tool.version,
            'date_version' : date_version,
            'rootback' : request.user.is_superuser
        })
    else:
        tool.name = request.POST['name']
        tool.version = request.POST['version']
        date_version = request.POST['date'].split('-')
        date_version = date(int(date_version[0]), int(date_version[1]), 1)

        tool.date_version = date_version
        tool.save()

        partes = str(date_version).split("-")[:2]
        date_version = "-".join(partes)
        
        return render(request, 'tools-form.html', {
            'name' : tool.name,
            'version' : tool.version,
            'date_version' : date_version,
            'success' : True,
            'rootback' : request.user.is_superuser
        })

def tool_delete(request, id_tool):
    try:
        tool = Tool.objects.get(id=id_tool)
        tool.delete()
    finally:
        return redirect(reverse('tools') + '?deleted=1')

def tool_update(request, id_tool):
    if request.method == 'GET':
        values = Tool_Category.objects.filter(tool_id=id_tool)
        tool = Tool.objects.get(id=id_tool)
        
        categories = Category.objects.all()
        categories = [{
            'id' : category.id,
            'topic' : category.topic,
            'value' : getattr(Tool_Category.objects.filter(tool_id=id_tool, category_id=category.id).first(), 'value', '0')
        } for category in categories]

        return render(request, 'form-update-tool.html', {
            'categories' : categories,
            'success' : False
        })
    else:
        items = list(request.POST.items()) 
        items.pop(0) # Quitamos el token csrf
        for key, value in items:
            register = key.split('-')
            id_category = register[1]
            try:
                tool_category = Tool_Category.objects.get(category_id=id_category, tool_id=id_tool)
                tool_category.value = value
                tool_category.save()
            except Tool_Category.DoesNotExist: 
                Tool_Category.objects.create(category_id=id_category, tool_id=id_tool, value=value)

        tool = Tool.objects.get(id=id_tool)
        if not tool.ready:
            tool.ready = 1
            tool.save()
        
        values = Tool_Category.objects.filter(tool_id=id_tool)

        categories = [{
            'id' : value.category_id,
            'topic' : Category.objects.get(id=value.category_id),
            'value' : value.value
        } for value in values]

        return render(request, 'form-update-tool.html', {
            'categories' : categories,
            'success' : True
        })

def categories(request):
    registered = request.GET.get('registered')
    deleted = request.GET.get('deleted')

    if registered:
        message = "The category has been registered successfully."
    elif deleted:
        message = "The category has been deleted successfully."
    else:
        message = ""

    flag = 1 if registered or deleted else 0

    categories = Category.objects.all()
    return render(request, 'categories.html', {
        'categories' : categories,
        'flag' : flag,
        'message' : message
    })

def category_new(request):
    if request.method == 'GET':
        tools = Tool.objects.all()
        return render(request, 'categories-form.html', {
            'tools' : tools
        })
    else:
        topic = request.POST['topic']

        try:
            if (Category.objects.get(topic=topic)):
                tools = Tool.objects.all()
                return render(request, 'categories-form.html', {
                    'tools' : tools,
                    'error' : True
                })

        except Category.DoesNotExist:
            description = request.POST['description']

            category = Category.objects.create(topic=topic, description=description)
            print(request.POST)

            for key, value in request.POST.items():
                if 'tool' in key:
                    id_tool = key.split('-')[1]
                    Tool_Category.objects.create(category_id=category.id, tool_id=id_tool, value=value)

            return redirect(reverse('categories') + '?registered=1')

def category_delete(request, id_category):
    try:
        category = Category.objects.get(id=id_category)
        category.delete()
    finally:
        return redirect(reverse('categories') + '?deleted=1')
        
def category_update(request, id_category):
    category = Category.objects.get(id=id_category)

    if request.method == 'GET':
        return render(request, 'categories-form.html', {
            'category' : category
        })
    else:
        category.topic = request.POST['topic']
        category.description = request.POST['description']

        category.save()
        
        return render(request, 'categories-form.html', {
            'category' : category,
            'success' : True
        })

def search(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, 'search.html', {
            'categories' : categories
        })
    else:
        selected_categories = []
        for key, value in request.POST.items():
            if key.isdigit():
                category_id = int(key)
                category = Category.objects.get(id=category_id)
                selected_categories.append(category)

        categories = [{"id": category.id, "topic": category.topic} for category in selected_categories]
        

        request.session['selected_categories'] = categories
        return redirect('order')

def survey(request):
    if request.method == 'GET':
        survey = Question.objects.exists()
        return render(request, 'survey.html', {
            'survey' : survey
        })
    else:
        try:
            file = request.FILES.get('file-survey')
            if file is None:
                return render(request, 'survey.html')

            json_file = json.load(file)

            if isinstance(json_file, list):

                if Question.objects.exists():
                    Question.objects.all().delete()

                for element in json_file:
                    question_text = element['question']
                    question = Question.objects.create(text=question_text)
                    answers = element['answers']
                    
                    for answer in answers:
                        Answer.objects.create(question_id=question.id, text=answer)

                return render(request, 'survey.html', {
                    'success' : True,
                    'survey' : True
                })
            else:
                return render(request, 'survey.html', {
                'error' : True
            })
        except:
            return render(request, 'survey.html', {
                'error' : True
            })

def order(request):
    if request.method == 'GET':
        categories_json = request.session.get('selected_categories')
        categories = json.dumps(categories_json)
        return render(request, 'order.html', {
            'categories': categories
        })
    else:
        
        critical_list = list(request.POST.getlist('critical'))
        standard_list = list(request.POST.getlist('standard'))
        optional_list = list(request.POST.getlist('optional'))

        request.session['critical_categories'] = critical_list
        request.session['standard_categories'] = standard_list
        request.session['optional_categories'] = optional_list

        return redirect('ranking')

def ranking(request):
    if request.method == 'GET':

        critical_list = request.session.get('critical_categories')
        standard_list = request.session.get('standard_categories')
        optional_list = request.session.get('optional_categories')

        len_critical = len(critical_list)
        len_standard = len(standard_list)
        len_optional = len(optional_list)

        total_length = len_critical + len_standard + len_optional

        matrix = [[0] * total_length for _ in range(total_length)]

        for i in range(total_length):
            for j in range(total_length):
                # Tratamos la diagonal, cualquier requisito comparado consigo mismo tiene importancia 1
                if i == j:
                    matrix[i][j] = 1
                # Tratamos los requisitos criticos...
                if i<len_critical: 
                    if j>len_critical-1 and j<total_length-len_optional: # ...comparados con los standard 
                        matrix[i][j] = 5
                    elif j>=total_length-len_optional and j<total_length: # ...comparados con los optional
                        matrix[i][j] = 7
                    else: # ...comparados con los critical
                        value = j-i
                        if (value<0):
                            value = 1/(abs(value)+1)
                        else:
                            value+=1
                        matrix[i][j] = value
                # Tratamos los requisitos standard...
                if i>=len_critical and i<total_length-len_optional:
                    if j<len_critical: # ...comparados con los critical
                        matrix[i][j] = 1/5
                    elif j>=total_length-len_optional and j<total_length: # ...comparados con los optional
                        matrix[i][j] = 5
                    else: # ...comparados con los standard
                        value = j-i
                        if (value<0):
                            value = 1/(abs(value)+1)
                        else:
                            value+=1
                        matrix[i][j] = value
                # Tratamos los requisitos optional...
                if i>=total_length-len_optional and i<total_length:
                    if j<len_critical: # ...comparados con los critical
                        matrix[i][j] = 1/7
                    elif j>len_critical-1 and j<total_length-len_optional: # ...comparados con los standard
                        matrix[i][j] = 1/5
                    else: # ...comparados con los optional
                        value = j-i
                        if (value<0):
                            value = 1/(abs(value)+1)
                        else:
                            value+=1
                        matrix[i][j] = value

        # Calculamos el total de cada columna
        sum_column = [0] * total_length 
        for j in range(total_length):
            sum_parcial = 0
            for i in range(total_length):
                sum_parcial += matrix[i][j]
            sum_column[j] = sum_parcial

        # Normalizamos la matriz: dividimos cada celda por el total de la columna
        for j in range(total_length):
            for i in range(total_length):
                matrix[i][j] = matrix[i][j]/sum_column[j]

        # Calculamos la media de cada fila
        priorities = np.mean(matrix, axis=1) # Prioridades de cada categoria
           
        categories = np.concatenate((critical_list, standard_list, optional_list))
        categories = categories.astype(int)

        # Obtenemos los índices que ordenan el array de prioridades
        idx = np.argsort(priorities)[::-1]

        # Hay que seleccionar cada herramienta en la tabla intermedia cuyo id sea de la categoria y de la herramienta y obtener el valor
        # Ese valor se saca de la DB y se multiplica por la prioridad de la categoria y así para todas las categorias
        # Se repite para cada herramienta
        tools = list(Tool.objects.filter(ready=1).values_list('id', flat=True))

        
        puntuations = [0]*len(tools) # Array para almacenar las puntuaciones finales de cada herramienta

        for t, tool in enumerate(tools):
            local_puntuation = 0.0;
            for c, category in enumerate(categories):
                tool_category = Tool_Category.objects.get(tool_id=tool, category_id=category)
                local_puntuation += tool_category.value*float(priorities[c])
                
            puntuations[t] = local_puntuation

        idx_puntuations = np.argsort(puntuations)[::-1] # Obtenemos los indices que ordenan las puntuaciones de mayor a menor valor
        idx_tools = np.minimum(len(puntuations), 10) # Por si hay menos de 10 herramientas
        idx_puntuations = idx_puntuations[:idx_tools]

        tools_ids = [tools[i] for i in idx_puntuations] # Lista con los ids de las herramientas
 
        rank_tools = []
        for i, id_tool in enumerate(tools_ids):
            tool_obj = Tool.objects.get(id=id_tool)
            vendor_obj = Vendor.objects.get(id=tool_obj.vendor_id)
            rank_tools.append({
                'name' : tool_obj.name,
                'vendor' : vendor_obj.name,
                'value' : round(puntuations[idx_puntuations[i]]/3*100, 2)
            })

        survey = Question.objects.exists()
        if (survey):
            questions = Question.objects.all()
            data = [{
                'question' : question,
                'answers' : list(Answer.objects.filter(question_id=question.id))
            } for question in questions]

        hide = request.GET.get('hide') or 0

        return render(request, 'ranking.html', {
            'tools': rank_tools,
            'survey' : '1' if survey else '0',
            'data' : data if survey else None,
            'hide' : hide
        })
    else:

        nickname = request.POST['nickname']        
        try:
            user = Survey_user.objects.get(nickname=nickname)
            user.count = user.count + 1
            user.save()
        except Survey_user.DoesNotExist:
            user = Survey_user.objects.create(nickname= nickname, count=1)

        for key, value in request.POST.items():
            if key.isdigit():
                id_answer = int(value)
                try:
                    user_answer = User_Answer.objects.get(answer_id=id_answer, user_id=user.id)
                    user_answer.count = user_answer.count + 1
                    user_answer.save()
                except User_Answer.DoesNotExist:
                    User_Answer.objects.create(answer_id=id_answer, user_id=user.id, count=1)

                critical_list = request.session.get('critical_categories')
                standard_list = request.session.get('standard_categories')
                optional_list = request.session.get('optional_categories')

                len_critical = len(critical_list)
                len_standard = len(standard_list)
                len_optional = len(optional_list)

                global_list = critical_list + standard_list + optional_list

                for i, id_category in enumerate(global_list):
                    if i<len_critical:
                        priority = 'critical'
                    elif i>=len_critical and i<len(global_list)-len_optional:
                        priority = 'standard'
                    else:
                        priority = 'optional'
                 
                    category = Category.objects.get(id=id_category)
                    try:
                        Category_Answer.objects.get(answer_id=id_answer, user_id=user.id, category_id=category.id, priority=priority)
                    except Category_Answer.DoesNotExist:
                        Category_Answer.objects.create(answer_id=id_answer, user_id=user.id, category_id=category.id, priority=priority)

        return redirect(reverse('ranking') + '?hide=1')
        

def delete_survey(request):
    if(Question.objects.exists()):
        Question.objects.all().delete()

    if(Survey_user.objects.exists()):
        Survey_user.objects.all().delete()

    return render(request, 'survey.html', {
        'success' : True
    }) 