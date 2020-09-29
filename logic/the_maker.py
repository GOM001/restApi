#!/usr/bin/env python
# coding: utf-8
try:
    from . import table
except:
    import table
import json


class maker:

    def __init__(self):
        fluxo = table.pg_table().fluxo
        self.fluxo = fluxo.loc[:,~fluxo.columns.duplicated()]

    def get_complet_json(self):
        json_to_dict = (self.fluxo.groupby(['codigo', 'dia_semana'])['periodo', 'faturamento']
            .apply(lambda x: x.to_dict('r'))
            .reset_index(name='data')
            .groupby('codigo')['dia_semana','data']
            .apply(lambda x: x.set_index('dia_semana')['data'].to_dict())
            .to_json())
        return json.loads(json_to_dict)
    
    def get_place_json(self, codigo):
        selc = self.fluxo.loc[self.fluxo['codigo'] == codigo].copy()
        selc.set_index(keys=['periodo', 'dia_semana'], inplace=True)
        selc.sort_index(inplace=True)
        return json.loads(selc.to_json(orient='index'))

if __name__ == "__main__":
    maker().get_complet_json()
