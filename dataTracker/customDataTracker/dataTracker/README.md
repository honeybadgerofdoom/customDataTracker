

Some Thoughts On Graphing

USE I-FRAMES!!

- Every user has 10
- They're populated from graph index 0 to graph index 9
- They're displayed in that same order in visualize.html
- No problem there, becuase only the later graphs are 'off', won't interfere
	with earlier graphs
- HOWEVER, when a used deletes a graph, you will need to 're-order' them as
	part of the route that deletes the graph in order to preserve the contraint
	that unused graphs must 'appear' after used graphs
	* To accomplish this 'reordering' you will need to:
		> Find index of deleted graph
		> Set all its fields to False/None
		> Use the copy constructor to shift every other graph 'up'
		> Set all fields of graph object at lowest index to False/None
- In visualize.html, check which datapoints are visible, only pass those lists
	to the chart.js stuff
	* Check which of those is 'on' for which graphs, add them to a list of lists
		> Iterate that outer list, create a graph for each inner list?




initializing database

python3

from datatracker import create_app
app = create_app()
app.app_context().push()
from datatracker import db

db.create_all()

from datatracker.models import User, DataPoint, DailyData, Graph