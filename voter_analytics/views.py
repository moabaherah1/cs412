# File: views.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 3 April 2025
# Description: Defines our classes
# Create your views here.

from django.views.generic import ListView, DetailView
from .models import *
from typing import Any
from django.db.models.query import QuerySet

from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import ExtractYear

import plotly
import plotly.graph_objects as go

class ResultsListView(ListView):
    '''View to display voter results'''
    template_name = 'voter_analytics/voter_list.html'
    model = Voter
    context_object_name = 'voter_list'
    paginate_by = 100
    
    def get_context_data(self, **kwargs):
        """Include the form in the template context"""
        context = super().get_context_data(**kwargs)
        context['years'] = range(1900, 2025)  
        context['voter_scores'] = range(1, 6)  
        return context

    def get_queryset(self):
        """Filter voter data based on form input"""
        queryset = super().get_queryset()

        party = self.request.GET.get('party')
        dob_min = self.request.GET.get('dob_min')
        dob_max = self.request.GET.get('dob_max')
        voter_score = self.request.GET.get('voter_score')
        voted_in = self.request.GET.getlist('voted_in')

        if party:
            queryset = queryset.filter(Party=party)
        if dob_min:
            queryset = queryset.filter(DOB__year__gte=dob_min)
        if dob_max:
            queryset = queryset.filter(DOB__year__lte=dob_max)
        if voter_score:
            queryset = queryset.filter(Voter_Score=voter_score)
        if voted_in:
            for election in voted_in:
                queryset = queryset.filter(**{election: "Yes"})
        
        return queryset
    
    
class VoterDetailView(DetailView):
    """View to display one voter"""

    model = Voter
    context_object_name = "v"
    template_name = 'voter_analytics/voter_detail.html'



class GraphsListView(ListView):
    """View to display graphs related to voter data"""

    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "voters"

    def get_queryset(self) -> QuerySet[Any]:
        """Apply filters to the queryset based on request parameters."""
        queryset = super().get_queryset()

        party = self.request.GET.get('party')
        dob_min = self.request.GET.get('dob_min')
        dob_max = self.request.GET.get('dob_max')
        voter_score = self.request.GET.get('voter_score')
        voted_in = self.request.GET.getlist('voted_in')

        if party:
            queryset = queryset.filter(Party=party)
        if dob_min:
            queryset = queryset.filter(DOB__year__gte=dob_min)
        if dob_max:
            queryset = queryset.filter(DOB__year__lte=dob_max)
        if voter_score:
            queryset = queryset.filter(Voter_Score=voter_score)
        if voted_in:
            for election in voted_in:
                queryset = queryset.filter(**{election: "Yes"})
        
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Generate graphs and add them to the context data"""
        context = super().get_context_data(**kwargs)

        voters = self.get_queryset()

        birth_year_counts = (
            voters.annotate(birth_year=ExtractYear("DOB"))
            .values("birth_year")
            .annotate(count=Count("id"))
            .order_by("birth_year")
        )

        # bar
        fig1 = go.Figure(
            data=[
                go.Bar(
                    x=[item["birth_year"] for item in birth_year_counts],
                    y=[item["count"] for item in birth_year_counts],
                )
            ]
        )

        fig1.update_layout(
            title="Voter Distribution by Birth Year",
            xaxis=dict(
                title="Birth Year",
                dtick=10,
                tickangle=45,
            ),
            yaxis=dict(
                title="Number of Voters",
            ),
        )

        context["birth_year_histogram_div"] = plotly.offline.plot(
            fig1, auto_open=False, output_type="div"
        )

        party_counts = voters.values("Party").annotate(count=Count("id"))

        fig2 = go.Figure(
            data=[
                go.Pie(
                    labels=[item["Party"] for item in party_counts],
                    values=[item["count"] for item in party_counts],
                )
            ]
        )
        fig2.update_layout(
            title="Voter Distribution by Party Affiliation",
        )
        context["party_pie_div"] = plotly.offline.plot(
            fig2, auto_open=False, output_type="div"
        )

        elections = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
        election_counts = [
            voters.filter(**{election: "Yes"}).count() for election in elections
        ]
        fig3 = go.Figure(
            data=[
                go.Bar(
                    x=elections,
                    y=election_counts,
                )
            ]
        )

        fig3.update_layout(
            title="Vote Count by Election",
            xaxis_title="Election",
            yaxis_title="Number of Voters",
        )

        context["election_bar_div"] = plotly.offline.plot(
            fig3, auto_open=False, output_type="div"
        )

        context['years'] = range(1900, 2025)  
        context['voter_scores'] = range(1, 6)
        context['current_party'] = self.request.GET.get('party', '')
        context['current_dob_min'] = self.request.GET.get('dob_min', '')
        context['current_dob_max'] = self.request.GET.get('dob_max', '')
        context['current_voter_score'] = self.request.GET.get('voter_score', '')
        context['current_voted_in'] = self.request.GET.getlist('voted_in')

        return context