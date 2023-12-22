import os
from flask import Flask,request,render_template
from datetime import date

app = Flask(__name__)


datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")


if 'tasks.txt' not in os.listdir('.'):
    with open('tasks.txt','w') as f:
        f.write('')


def gettasklist():
    with open('tasks.txt','r') as f:
        tasklist = f.readlines()
    return tasklist

def createnewtasklist():
    os.remove('tasks.txt')
    with open('tasks.txt','w') as f:
        f.write('')

def updatetasklist(tasklist):
    os.remove('tasks.txt')
    with open('tasks.txt','w') as f:
        f.writelines(tasklist)


@app.route('/')
def home():
    return render_template('home.html',datetoday2=datetoday2,tasklist=gettasklist(),l=len(gettasklist())) 


@app.route('/clear')
def clear_list():
    createnewtasklist()
    return render_template('home.html',datetoday2=datetoday2,tasklist=gettasklist(),l=len(gettasklist())) 


@app.route('/addtask',methods=['POST'])
def add_task():
    task = request.form.get('newtask')
    with open('tasks.txt','a') as f:
        f.writelines(task+'\n')
    return render_template('home.html',datetoday2=datetoday2,tasklist=gettasklist(),l=len(gettasklist())) 


@app.route('/deltask',methods=['GET'])
def remove_task():
    task_index = int(request.args.get('deltaskid'))
    tasklist = gettasklist()
    print(task_index)
    print(tasklist)
    if task_index < 0 or task_index > len(tasklist):
        return render_template('home.html',datetoday2=datetoday2,tasklist=tasklist,l=len(tasklist),mess='Invalid Index...') 
    else:
        removed_task = tasklist.pop(task_index)
    updatetasklist(tasklist)
    return render_template('home.html',datetoday2=datetoday2,tasklist=tasklist,l=len(tasklist)) 
    

if __name__ == '__main__':
    app.run(debug=True)