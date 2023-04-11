<h2>About This Directory</h2>

This directory contains the backend for running the simulations.
<br></br>
<ul>
  <li>Data.py contains the data management such as querying the database or yfinance based on user requests.</li>
  <li>Strategies.py contains all the strategies available for testing.</li>
  <li>Simulation.py calculated the technical indicator values, trade entries and exits, and the resulting portfolio results. It also serves as the primary input to components with callbacks, providing datatables and plots.</li>
</ul>