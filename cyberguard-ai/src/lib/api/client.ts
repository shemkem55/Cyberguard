import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface Asset {
    id: number;
    name: string;
    type: string;
    ip_address: string;
    criticality: number;
}

export interface Vulnerability {
    id: number;
    cve_id: string;
    title: string;
    severity: number;
    status: string;
}

export const getAssets = async (): Promise<Asset[]> => {
    const response = await apiClient.get('/assets');
    return response.data;
};

export const getVulnerabilities = async (): Promise<Vulnerability[]> => {
    const response = await apiClient.get('/vulnerabilities');
    return response.data;
};
