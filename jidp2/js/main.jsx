import React from 'react';
import ReactDOM from 'react-dom';
// import Likes from './likes';
// import Post from './posts';

// This method is only called once
ReactDOM.render(
  <InfScroll url="/api/v1/p/" />,
  document.getElementById('reactEntry'),
);
