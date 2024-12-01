import React from 'react';
import StatPageTemplate from '../../../components/StatPageTemplate';

export default function TeamsPage({ params }) {
  const { league } = React.use(params);
  return <StatPageTemplate league={league} stat="Teams" />;
}

