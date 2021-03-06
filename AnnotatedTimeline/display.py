# -------------------------------------------------------------------------------
# Generated by PixieDust code generator
# 
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Inherited from maven-artifact https://github.com/hamnis/maven-artifact
# -------------------------------------------------------------------------------

from pixiedust.display.display import Display
from pixiedust.utils import Logger

from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.palettes import Category10
from bokeh.models import Span, Label, Legend, LegendItem
from bokeh.settings import settings

from bokeh.models import DatetimeTickFormatter
from bokeh.util.notebook import load_notebook

import datetime as dt
import string
import time

@Logger()
class AnnotatedTimelineHandler(Display):
    """
        Main Render method
    """
    def doRender(self,handlerId):
        #TODO Add your code here
        #You can use the methods available in base Display class to construct the html markup that will be sent to the output cell
        load_notebook(hide_banner=True)
        #output_notebook()
        workingPDF = self.entity.copy()
        keyFields = self.options.get("keyFields")
        valueFields = self.options.get("valueFields")
        serValues = self.options.get("seriesValues")
        eventField = self.options.get("eventField")

        ht = self.options.get("height")
        wdth = self.options.get("width")

        workingPDF[keyFields] = [dt.datetime.strptime(str(x), "%Y%m%d") for x in workingPDF[keyFields]]
        fig = figure(height=int(ht), width=int(wdth), x_axis_type="datetime")
        fig.xaxis.formatter = DatetimeTickFormatter(days="%D")


        sArr = serValues.split(",")
        numSeries = len(sArr)

        #fig.logo = None
        fig.toolbar_location = None

        cols = Category10[numSeries]
        i = 0

        for s in sArr:
            cat = workingPDF[workingPDF['name'] == s]
            fig.line(cat[keyFields], cat[valueFields], line_width=2, color=cols[i], legend=s)
            i = i+1

        fig.legend.location = "top_left"
        fig.legend.background_fill_color = "white"
        fig.legend.background_fill_alpha = 0.8
        fig.legend.click_policy = "hide"

        lblArr = list(string.ascii_uppercase)
        cat = workingPDF[workingPDF['name'] == eventField]
        cat.sort_values([keyFields], ascending = [True], inplace=True)

        sparr = []
        i = 0
        lits = []

        spmap = {}
        for idx, row in cat.iterrows():
            k = time.mktime(row[keyFields].timetuple()) * 1000
            lpos = int(ht) - 30

            if k in spmap:
                lpos = spmap[k] - 30

            #self.debug("----- " + str(k) +  " : " + lblArr[i] + " -------")
            sparr.append(Span(location=k, dimension='height', line_color='black'))
            lbl = Label(x=k+10000000, y=lpos, y_units='screen', text=lblArr[i], render_mode='css',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0)
            fig.add_layout(lbl)
            lits.append(LegendItem(label=lblArr[i] + " : " + row['description']))
            i = i + 1
            spmap[k] = lpos

        fig.renderers.extend(sparr)
        fig.add_layout(Legend(items=lits, location=(0, 10)), 'right')

        #show(fig)
        html = file_html(fig, CDN)
        self._addHTMLTemplateString(html)

        #Add html from a jinja2 template, the file must be located in the templates folder located under this file

        #Note: you can embed the HTML directly in the file like so
        #self._addHTMLTemplateString("<div>Hello World</div>")