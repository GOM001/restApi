#!/usr/bin/env python
# coding: utf-8
try:
    from . import table
except:
    import table
import json
import numpy as np


class maker:

    def __init__(self):
        fluxo = table.pg_table().fluxo
        self.fluxo = fluxo.loc[:,~fluxo.columns.duplicated()]
        self.list_cods = np.array(self.fluxo['codigo'].unique().tolist())
        self.arrays = np.array_split( self.list_cods, int(len(self.list_cods)/50))

    def get_complet_json(self, list_):
        fluxo = self.fluxo[self.fluxo['codigo'].isin(list_)]
        json_to_dict = (fluxo.groupby(['codigo', 'dia_semana'])['periodo', 'faturamento']
            .apply(lambda x: x.to_dict('r'))
            .reset_index(name='data')
            .groupby('codigo')['dia_semana','data']
            .apply(lambda x: x.set_index('dia_semana')['data'].to_dict())
            .to_json())
        return json.loads(json_to_dict)
    
    def get_list(self):
        json_ = {}
        for n, y in enumerate(self.arrays):
            json_[f'Pagina {n+1}'] = [str(x) for x in (list(y))]
        json_['numero de paginas'] = len(self.arrays)
        json_['Quantidade Total de Concorrentes'] = len(self.list_cods)
        fluxo_unique = self.fluxo[['codigo', 'faixa_preco']].copy().drop_duplicates()
        faixa_preco = fluxo_unique['faixa_preco'].value_counts().to_dict()
        json_['Concorrentes por falxa de preço'] = faixa_preco
        return json_

    def get_pag(self, pag):
        pag_cods = self.arrays[pag]
        list_ = [str(x) for x in (list(pag_cods))]
        json_ = self.get_complet_json(list_)
        return json_
    
    def get_place_json(self, codigo):
        selc = self.fluxo.loc[self.fluxo['codigo'] == codigo].copy()
        selc.set_index(keys=['dia_semana', 'periodo'], inplace=True)
        selc.sort_index(inplace=True)
        return json.loads(selc.to_json(orient='index'))

if __name__ == "__main__":
    maker().get_complet_json()
