from django.shortcuts import render
from django.views.generic import View
from .updatedata import write
import random
from .models import IndiaTimeSeries, State, ImpParam, District,GovernmentHelpline,TestCenters,ConfirmedTimeSeriesState,RecoveredTimeSeriesState,DeathsTimeSeriesState
# Create your views here.


class India(View):
    mytemplate = 'india_status.html'
    unsupported = 'Unsupported operation'
    def get(self, request):
        indconfirmed = ImpParam.objects.get(key="indconfirmed").value
        indactive = ImpParam.objects.get(key="indactive").value
        inddeaths = ImpParam.objects.get(key="inddeaths").value
        indrecovered = ImpParam.objects.get(key="indrecovered").value
        inddeltadeaths = ImpParam.objects.get(key="inddeltadeaths").value
        inddeltaconfirmed = ImpParam.objects.get(key="inddeltaconfirmed").value
        inddeltarecovered = ImpParam.objects.get(key="inddeltarecovered").value
        totalindividualtested = ImpParam.objects.get(key="totalindividualtested").value
        totalsampletested = ImpParam.objects.get(key="totalsampletested").value
        lastupdated = ImpParam.objects.get(key="indlastupdatetime").value

        statedata = State.objects.all().filter(confirmed__gte=10).order_by('-confirmed')

        indiatimeseries = IndiaTimeSeries.objects.all()
        indiatimeserieslabel = []
        indiatimeseriesdailydata = []
        inditimeseriescummdata = []
        barcolorlist = []
        statenameslabel = []
        statecasedata=[]
        barcolorlistforstate = []
        for tcs in indiatimeseries:
            indiatimeserieslabel.append(tcs.date)
            indiatimeseriesdailydata.append(tcs.dailyconfirmed)
            # clr = "rgba("+str(int(tcs.dailyconfirmed/255)*10+100)+", 30, 30, 0.2)"
            barcolorlist.append('rgba(255, 99, 132, 0.2)',)
            inditimeseriescummdata.append(tcs.totalconfirmed)


        mapdatalist = [['State', 'Count']]
        for st in statedata:
            statenameslabel.append(st.name)
            statecasedata.append(st.confirmed)
            mapdatalist.append([st.name,st.confirmed])
            clr = 'rgba('+str(random.randint(1, 10)*25)+','+str(random.randint(1, 10)*25)+','+str(random.randint(1, 10)*25)+','+'0.4';
            barcolorlistforstate.append(clr)


        top5namelabel = []
        top5data = []
        topstate = statedata[0:5]
        top5 = {}
        for tpss in topstate:
            distr = District.objects.all().filter(state=tpss).order_by('-confirmed')
            top5.update({tpss:distr})
            top5namelabel.append(tpss.name)
            top5data.append(tpss.confirmed)

        # for inn in indiatimeseries:
        #     print(inn.date)

        context = {
            'indconfirmed':indconfirmed,
            'indactive':indactive,
            'inddeaths':inddeaths,
            'indrecovered':indrecovered,
            'totalindividualtested':totalindividualtested,
            'totalsampletested':totalsampletested,
            'indiatimeserieslabel':indiatimeserieslabel,
            'indiatimeseriesdailydata':indiatimeseriesdailydata,
            'barcolorlist':barcolorlist,
            'inditimeseriescummdata':inditimeseriescummdata,
            'statenameslabel':statenameslabel,
            'statecasedata':statecasedata,
            'statedata':statedata,
            'top5':top5,
            'mapdatalist':mapdatalist,
            'top5data':top5data,
            'top5namelabel':top5namelabel,
            'barcolorlistforstate':barcolorlistforstate,
            'lastupdated':lastupdated,
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)



class StateView(View):
    mytemplate = 'state_status.html'
    unsupported = 'Unsupported operation'
    def get(self, request, statecode):
        lastupdated = ImpParam.objects.get(key="indlastupdatetime").value

        state = State.objects.get(statecode=statecode)
        districts = District.objects.all().filter(state=state).order_by('-confirmed')

        confirmseries = ConfirmedTimeSeriesState.objects.all()
        datelabel = []
        datacumm = []
        datadaily = []
        barcolorlist=[]
        i=0
        callf = (statecode[-2]+statecode[-1]).lower()+"i"
        for cnf in confirmseries:
            datelabel.append(cnf.date)
            datadaily.append(getattr(cnf, callf))
            if(i==0):
                datacumm.append(getattr(cnf, callf))
            else:
                datacumm.append((datacumm[i-1]+getattr(cnf, callf)))
            clr = 'rgba('+str(random.randint(1, 10)*25)+','+str(random.randint(1, 10)*25)+','+str(random.randint(1, 10)*25)+','+'0.4';
            barcolorlist.append(clr)
            i = i+1


        context = {
            'state':state,
            'datacumm':datacumm,
            'datadaily':datadaily,
            'datelabel':datelabel,
            'districts':districts,
            'barcolorlist':barcolorlist,
            'lastupdated':lastupdated,
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)


class StateTable(View):

    mytemplate = 'states_table.html'
    unsupported = 'Unsupported operation'
    def get(self, request):

        states = State.objects.all().filter(confirmed__gte=1).order_by('-confirmed')
        statedata = {}

        for sta in states:
            distr = District.objects.all().filter(state=sta).order_by('-confirmed')
            statedata.update({sta:distr})
        context = {
            'statedata':statedata,
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)


class Helpline(View):
    mytemplate = 'helpline.html'
    unsupported = 'Unsupported operation'
    def get(self, request):

        testcenters = TestCenters.objects.all()
        helplines = GovernmentHelpline.objects.all()

        context = {
            'testcenters':testcenters,
            'helplines':helplines,
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)
