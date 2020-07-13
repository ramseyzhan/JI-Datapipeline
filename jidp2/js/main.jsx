import React from 'react';
import ReactDOM from 'react-dom';
import Index from './index';

// This method is only called once
ReactDOM.render(
  <Index url="/api/v1/" />,
  document.getElementById('reactEntry'),
);
