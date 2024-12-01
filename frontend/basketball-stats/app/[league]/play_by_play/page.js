import React from 'react';
import StatPageTemplate from '../../../components/StatPageTemplate';

export default function PlayByPlayPage({ params }) {
  const { league } = React.use(params);
  return <StatPageTemplate league={league} stat="Play by Play" />;
}

