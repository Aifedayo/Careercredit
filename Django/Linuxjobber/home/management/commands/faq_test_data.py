from django.core.management.base import BaseCommand
from home.models import FAQ, werole, wetype, wetask ,wework, wepeoples
from  users.models import CustomUser
from datetime import  timedelta
from home.management.fake_data import get_wetask_data
import datetime
import random
import json


start_date = datetime.datetime.now() - timedelta(days=47)
wtype = wetype.objects.get(pk=1)

#unique username generator helper
def generate_unique_username():
    username = 'test'
    while True:
        random_number = random.randint(1000, 9999)
        if not CustomUser.objects.filter(
            username=username + str(random_number)
        ).exists():
            username = username + str(random_number)
            break
    return username

def generate_unique_wetask_weight(typ):
    weight = 0
    while True:
        random_number = random.randint(1000, 9999)
        if not wetask.objects.filter(
            types=typ, weight= random_number
        ).exists():
            weight = random_number
            break
    return weight

def generate_unique_wework_weight(we_people):
    weight = 0
    while True:
        random_number = random.randint(1000, 9999)
        if not wework.objects.filter(
            we_people=we_people, weight=random_number
        ).exists():
            weight = random_number
            break
    return weight

def get_user(u={}):
    username = u.get('username', generate_unique_username())
    random_number = random.randint(1000, 9999)
    user = CustomUser(
        username=username,
        email=username+'@mail.com',
        first_name=u.get(
            'first_name', 'first'+ str(random_number),
        ),
        last_name=u.get(
            'last_name', 'last'+ str(random_number),
        ),
    )
    user.set_password('password@1')
    user.save()
    return user

def get_wepoeple(u):
    user = get_user(u)
    wepeople = wepeoples(
        user=user,
        profile_picture=None,
        person=werole.objects.get(pk=1),
        current_position='Enginer',
        state='Lagos',
        income='0',
        relocation=None,
        Paystub=None,
        last_verification=None,
        start_date=start_date,
        graduation_date=start_date + timedelta(days=90),
        types=wtype
    )
    wepeople.save()
    return wepeople

def get_wetask(wtask):
    wetsk = wetask(
        weight=generate_unique_wetask_weight(wtype),
        task=wtask['task'],
        objective=wtask['task'],
        description=wtask['task'],
        created=start_date - timedelta(days=10),
        is_active=1,
        types=wtype,
        group=1
    )
    wetsk.save()
    return wetsk

def get_wework(wep, task):
    random_time = random.randint(2, 20)
    created_time = start_date + timedelta(days=random_time)
    wwork = wework(
        weight=generate_unique_wework_weight(wep),
        we_people=wep,
        task=task,
        status=1,
        created=created_time,
        send_task=1,
        due=created_time + timedelta(days=3)
    )
    wwork.save()
    return wwork


class Command(BaseCommand):

    def add_arguments(self, parser):
        return super().add_arguments(parser)

    def handle(self, *args, **kwargs):
        self.clear_db()

        wetasks = []
        for wtask in get_wetask_data():
           wetasks.append(get_wetask(wtask))

        wep1 = get_wepoeple({
            'username':'wetest1'
        })
        
        # self.stdout.write(
        #     json.dumps(get_wepoeple({}))
        # )

        for wt in wetasks:
            get_wework(wep1, wt)

        wep2 = get_wepoeple({
            'username':'wetest2'
        })

        get_wework(wep2, wetasks[0])

        self.stdout.write(
            self.style.SUCCESS(
                'Dumy Test Data successfully seeded'
            )
        )

    def clear_db(self):
        wetasks = []
        for wtask in get_wetask_data():
            wetasks.append(wtask['task'])
        wetask.objects.filter(task__in=wetasks).delete()

        qs = CustomUser.objects.filter(
            username='wetest1'
        )|CustomUser.objects.filter(username='wetest2')
        qs.delete()