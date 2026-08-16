const API_BASE_URL = 'http://localhost:8000/api';

export const apiService = {
  async getCandidates() {
    const res = await fetch(`${API_BASE_URL}/candidates`);
    if (!res.ok) throw new Error('Failed to fetch candidate sites');
    return res.json();
  },

  async getHospitals() {
    const res = await fetch(`${API_BASE_URL}/hospitals`);
    if (!res.ok) throw new Error('Failed to fetch hospitals');
    return res.json();
  },

  async getStatistics() {
    const res = await fetch(`${API_BASE_URL}/statistics`);
    if (!res.ok) throw new Error('Failed to fetch statistics');
    return res.json();
  },

  async updateScenario(scenarioData) {
    const res = await fetch(`${API_BASE_URL}/scenario`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(scenarioData)
    });
    if (!res.ok) throw new Error('Failed to recalculate scenario');
    return res.json();
  },

  async queryAI(query, siteA = null, siteB = null) {
    const res = await fetch(`${API_BASE_URL}/ai/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, site_id_a: siteA, site_id_b: siteB })
    });
    if (!res.ok) throw new Error('Failed to query AI engine');
    return res.json();
  },

  async getDataSources() {
    const res = await fetch(`${API_BASE_URL}/data-sources`);
    if (!res.ok) throw new Error('Failed to fetch data sources');
    return res.json();
  }
};