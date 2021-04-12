from django.http import HttpResponseRedirect
from django.shortcuts import render

from board import models


def index(request):
    contenslist = models.findall_list()
    data = {'contenslist': contenslist}

    return render(request, 'board/index.html', data)


def view(request):
    no = request.GET['no']
    contents = models.findall_contents(no)
    data = {'contents': contents[0]}

    hit = contents[0]['hit'] +1
    models.update_hit(hit, no)

    return render(request, 'board/view.html', data)


def updateform(request):
    no = request.GET['no']
    contents = models.findall_contents(no)
    data = {'contents': contents[0]}
    print(data['contents'])

    return render(request, 'board/updateform.html', data)


def update(request):
    title = request.POST['title']
    contents = request.POST['content']
    no = request.GET['no']

    models.update(title, contents, no)

    return HttpResponseRedirect('/board/views?no='+no)


def writeform(request):
    # 로그인 확인
    authuser = request.session.get('authuser')
    if authuser is None:
        return HttpResponseRedirect('/user/reqlogin')
    # 넘김
    return render(request, 'board/writeform.html')


def write(request):
    title = request.POST['title']
    contents = request.POST['content']
    user_no = request.GET['no']
    g_no = models.find_max_g_no()
    if g_no is None:
        g_no = 1

    models.insert(title, contents, g_no, user_no)

    return HttpResponseRedirect('/board')


def replyform(request):
    # 로그인 확인
    authuser = request.session.get('authuser')
    if authuser is None:
        return HttpResponseRedirect('/user/reqlogin')

    contents = models.findall_contents(request.GET['no'])
    data = {'contents': contents[0]}

    return render(request, 'board/replyform.html', data)


def reply(request):
    title = request.POST['title']
    contents = request.POST['content']
    g_no = request.POST['g_no']
    o_no = int(request.POST['o_no'])+1
    depth = int(request.POST['depth'])+1

    authuser = request.session.get('authuser')
    user_no = authuser['no']

    models.reply(title, contents, g_no, o_no, depth, user_no)

    return HttpResponseRedirect('/board')


def delete(request):
    # 로그인 확인
    authuser = request.session.get('authuser')
    if authuser is None:
        return HttpResponseRedirect('/user/reqlogin')

    no = request.GET['no']
    user_no = authuser['no']
    result = models.delete(no, user_no)

    if result:
        return HttpResponseRedirect('/board')

    else:
        return HttpResponseRedirect('/board/delete')


def deletealert(request):

    return render(request, 'board/delete.html')


def search(request):
    kwd = request.POST['kwd']

    return HttpResponseRedirect('/board/search?kwd='+kwd)


def searchlist(request):
    kwd = request.GET['kwd']
    kwd = '%'+kwd+'%'
    contenslist = models.search(kwd)
    data = {'contenslist': contenslist}

    return render(request, 'board/search.html', data)