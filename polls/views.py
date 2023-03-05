import json

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
# Create your views here.
from .models import Question, Choice
from django.urls import reverse


import paramiko
import re
from time import sleep


# request 不要漏
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # if isinstance(question_id, int):
    #     return HttpResponse(f"You're looking at question {question_id}, it is int")
    # elif isinstance(question_id, str):
    #     return HttpResponse(f"You're looking at question {question_id}, it is str")

    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Exception as e:
    #     raise Http404(f'___>{e}')

    # question = Question.objects.get(pk=question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question1': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def results(request, question_id):
    # response = f"You're looking at the results of question {question_id}"
    # return HttpResponse(response)

    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

class Linux(object):
    # 通过IP, 用户名，密码，超时时间初始化一个远程Linux主机
    def __init__(self, ip, username, password, timeout=30):
        self.ip = ip
        self.username = username
        self.password = password
        self.timeout = timeout


        # transport和chanel
        self.t = None
        self.chan = None
        # 链接失败的重试次数
        self.try_times = 3

    # 调用该方法连接远程主机
    def connect(self):
        while True:
            # 连接过程中可能会抛出异常，比如网络不通、链接超时
            try:
                self.t = paramiko.Transport(sock=(self.ip, 22))
                self.t.connect(username=self.username, password=self.password)
                self.chan = self.t.open_session()
                self.chan.settimeout(self.timeout)
                self.chan.get_pty()
                self.chan.invoke_shell()
                # 如果没有抛出异常说明连接成功，直接返回
                print(u'连接%s成功' % self.ip)
                # 接收到的网络数据解码为str
                print(self.chan.recv(65535).decode('utf-8'))
                return
            # 这里不对可能的异常如socket.error, socket.timeout细化，直接一网打尽
            except Exception:
                if self.try_times != 0:
                    print(u'连接%s失败，进行重试' % self.ip)
                    self.try_times -= 1
                else:
                    print(u'重试3次失败，结束程序')
                    exit(1)

    # 断开连接
    def close(self):
        self.chan.close()

        self.t.close()

    # 发送要执行的命令
    def send(self, cmd, pattern):
        cmd += '\r'
        # 通过命令执行提示符来判断命令是否执行完成
        patt = pattern
        p = re.compile(patt)
        result = ''
        # 发送要执行的命令
        self.chan.send(cmd)
        # 回显很长的命令可能执行较久，通过循环分批次取回回显
        while True:
            sleep(0.5)
            ret = self.chan.recv(65535)
            ret = ret.decode('utf-8')
            result += ret
            if p.search(ret):
                print(result)
                return result

    # 上传
    def upload(self):
        src_file = '/Users/shihuajun/Documents/Library/Python-UIAutomation.pdf'
        dsc_path = '/tmp/Python-UIAutomation.pdf'
        sftp = paramiko.SFTPClient.from_transport(self.t)
        try:
            sftp.put(src_file,dsc_path)
        except Exception as e:
            print(e)

    # 下载
    def down(self, server_path, localpath):
        try:
            # Open a transport
            host, port = "example.com", 22
            transport = paramiko.Transport((self.ip, port))

            # Auth
            # username, password = "bar", "foo"
            # None --> pay attention otherwise it won't pass
            # https://stackoverflow.com/questions/3635131/paramikos-sshclient-with-sftp
            # https://docs.paramiko.org/en/stable/api/transport.html#paramiko.transport.Transport.connect
            transport.connect(None, self.username, self.password)

            # Go!
            sftp = paramiko.SFTPClient.from_transport(transport)

            sftp.get(server_path, localpath)

            if sftp: sftp.close()
            if transport: transport.close()

        except Exception as e:
            print(e)

    def exec(self):
        ...

l1 = Linux('47.100.25.73', 'root', '@alyshj)OKM0okm', timeout=30)
l1.connect()
l1.upload()

def operlinux(request):
    # res = l1.send('cd /tmp;ll', '.')
    res = l1.send('cat /root/config/test.txt', '.')
    return HttpResponse(f'{res}')

def mock_user(request):
    data = {'name': '小张', 'age': 18 }
    return HttpResponse(f'hellp')

def active_app(request):
    # num = 1234
    app_info = {
       'total_apps_num': 3200,
        'up_apps_num': 2830,
    }
    app_info = json.dumps(app_info)
    # print(app_info)
    return HttpResponse(f'{app_info}')

def time_trace(request):
    print(request)
    data = request.body
    print(data)
    # print(data.get('input_pid'))
    # print(data.get('input_ip'))
    time_info = ['app1- ip, time', '--|app2 - ip , time', '--|--|app3 - ip , time']
    time_info = json.dumps(time_info)
    return HttpResponse(f'{time_info}')

