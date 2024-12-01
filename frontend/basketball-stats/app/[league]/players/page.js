import React from 'react';
import StatPageTemplate from '../../../components/StatPageTemplate';

export default function PlayersPage({ params }) {
  const { league } = React.use(params);
  return <StatPageTemplate league={league} stat="Players" />;
}

