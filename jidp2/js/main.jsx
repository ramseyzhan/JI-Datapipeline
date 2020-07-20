import React from 'react';
import ReactDOM from 'react-dom';
import Anomaly from './anomaly';

// This method is only called once
ReactDOM.render(
  <Anomaly url="/api/v1/m/" />,
  document.getElementById('reactEntry'),
);
