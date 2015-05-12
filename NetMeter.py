#!/usr/bin/python3
#
# Copyright (c) 2015, Daynix Computing LTD (www.daynix.com)
# All rights reserved.
#
# Maintained by bricklets@daynix.com
#
# This file is a part of Bricklets library, see "Bricklets" page
# on www.daynix.com for more.
#
# This code is licensed under standard 3-clause BSD license.
# See file LICENSE supplied with this package for the full license text.

import numpy as np
import sys
import signal
from datetime import datetime, timedelta
from time import sleep
from subprocess import Popen
from os import makedirs
from os.path import isdir, join


rundate = datetime.now().strftime('%Y_%m_%d_%H-%M-%S')
daynix_logo = (
               'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGkAAAAUCAYAAACOPhMlAAAABGdBTUEAALGPC/xhBQAACjFpQ0NQ'
               'SUNDIFByb2ZpbGUAAEiJnZZ3VFPZFofPvTe9UJIQipTQa2hSAkgNvUiRLioxCRBKwJAAIjZEVHBE'
               'UZGmCDIo4ICjQ5GxIoqFAVGx6wQZRNRxcBQblklkrRnfvHnvzZvfH/d+a5+9z91n733WugCQ/IMF'
               'wkxYCYAMoVgU4efFiI2LZ2AHAQzwAANsAOBws7NCFvhGApkCfNiMbJkT+Be9ug4g+fsq0z+MwQD/'
               'n5S5WSIxAFCYjOfy+NlcGRfJOD1XnCW3T8mYtjRNzjBKziJZgjJWk3PyLFt89pllDznzMoQ8Gctz'
               'zuJl8OTcJ+ONORK+jJFgGRfnCPi5Mr4mY4N0SYZAxm/ksRl8TjYAKJLcLuZzU2RsLWOSKDKCLeN5'
               'AOBIyV/w0i9YzM8Tyw/FzsxaLhIkp4gZJlxTho2TE4vhz89N54vFzDAON40j4jHYmRlZHOFyAGbP'
               '/FkUeW0ZsiI72Dg5ODBtLW2+KNR/Xfybkvd2ll6Ef+4ZRB/4w/ZXfpkNALCmZbXZ+odtaRUAXesB'
               'ULv9h81gLwCKsr51Dn1xHrp8XlLE4ixnK6vc3FxLAZ9rKS/o7/qfDn9DX3zPUr7d7+VhePOTOJJ0'
               'MUNeN25meqZExMjO4nD5DOafh/gfB/51HhYR/CS+iC+URUTLpkwgTJa1W8gTiAWZQoZA+J+a+A/D'
               '/qTZuZaJ2vgR0JZYAqUhGkB+HgAoKhEgCXtkK9DvfQvGRwP5zYvRmZid+8+C/n1XuEz+yBYkf45j'
               'R0QyuBJRzuya/FoCNCAARUAD6kAb6AMTwAS2wBG4AA/gAwJBKIgEcWAx4IIUkAFEIBcUgLWgGJSC'
               'rWAnqAZ1oBE0gzZwGHSBY+A0OAcugctgBNwBUjAOnoAp8ArMQBCEhcgQFVKHdCBDyByyhViQG+QD'
               'BUMRUByUCCVDQkgCFUDroFKoHKqG6qFm6FvoKHQaugANQ7egUWgS+hV6ByMwCabBWrARbAWzYE84'
               'CI6EF8HJ8DI4Hy6Ct8CVcAN8EO6ET8OX4BFYCj+BpxGAEBE6ooswERbCRkKReCQJESGrkBKkAmlA'
               '2pAepB+5ikiRp8hbFAZFRTFQTJQLyh8VheKilqFWoTajqlEHUJ2oPtRV1ChqCvURTUZros3RzugA'
               'dCw6GZ2LLkZXoJvQHeiz6BH0OPoVBoOhY4wxjhh/TBwmFbMCsxmzG9OOOYUZxoxhprFYrDrWHOuK'
               'DcVysGJsMbYKexB7EnsFO459gyPidHC2OF9cPE6IK8RV4FpwJ3BXcBO4GbwS3hDvjA/F8/DL8WX4'
               'RnwPfgg/jp8hKBOMCa6ESEIqYS2hktBGOEu4S3hBJBL1iE7EcKKAuIZYSTxEPE8cJb4lUUhmJDYp'
               'gSQhbSHtJ50i3SK9IJPJRmQPcjxZTN5CbiafId8nv1GgKlgqBCjwFFYr1Ch0KlxReKaIVzRU9FRc'
               'rJivWKF4RHFI8akSXslIia3EUVqlVKN0VOmG0rQyVdlGOVQ5Q3mzcovyBeVHFCzFiOJD4VGKKPso'
               'ZyhjVISqT2VTudR11EbqWeo4DUMzpgXQUmmltG9og7QpFYqKnUq0Sp5KjcpxFSkdoRvRA+jp9DL6'
               'Yfp1+jtVLVVPVb7qJtU21Suqr9XmqHmo8dVK1NrVRtTeqTPUfdTT1Lepd6nf00BpmGmEa+Rq7NE4'
               'q/F0Dm2OyxzunJI5h+fc1oQ1zTQjNFdo7tMc0JzW0tby08rSqtI6o/VUm67toZ2qvUP7hPakDlXH'
               'TUegs0PnpM5jhgrDk5HOqGT0MaZ0NXX9dSW69bqDujN6xnpReoV67Xr39An6LP0k/R36vfpTBjoG'
               'IQYFBq0Gtw3xhizDFMNdhv2Gr42MjWKMNhh1GT0yVjMOMM43bjW+a0I2cTdZZtJgcs0UY8oyTTPd'
               'bXrZDDazN0sxqzEbMofNHcwF5rvNhy3QFk4WQosGixtMEtOTmcNsZY5a0i2DLQstuyyfWRlYxVtt'
               's+q3+mhtb51u3Wh9x4ZiE2hTaNNj86utmS3Xtsb22lzyXN+5q+d2z31uZ27Ht9tjd9Oeah9iv8G+'
               '1/6Dg6ODyKHNYdLRwDHRsdbxBovGCmNtZp13Qjt5Oa12Oub01tnBWex82PkXF6ZLmkuLy6N5xvP4'
               '8xrnjbnquXJc612lbgy3RLe9blJ3XXeOe4P7Aw99D55Hk8eEp6lnqudBz2de1l4irw6v12xn9kr2'
               'KW/E28+7xHvQh+IT5VPtc99XzzfZt9V3ys/eb4XfKX+0f5D/Nv8bAVoB3IDmgKlAx8CVgX1BpKAF'
               'QdVBD4LNgkXBPSFwSGDI9pC78w3nC+d3hYLQgNDtoffCjMOWhX0fjgkPC68JfxhhE1EQ0b+AumDJ'
               'gpYFryK9Issi70SZREmieqMVoxOim6Nfx3jHlMdIY61iV8ZeitOIE8R1x2Pjo+Ob4qcX+izcuXA8'
               'wT6hOOH6IuNFeYsuLNZYnL74+BLFJZwlRxLRiTGJLYnvOaGcBs700oCltUunuGzuLu4TngdvB2+S'
               '78ov508kuSaVJz1Kdk3enjyZ4p5SkfJUwBZUC56n+qfWpb5OC03bn/YpPSa9PQOXkZhxVEgRpgn7'
               'MrUz8zKHs8yzirOky5yX7Vw2JQoSNWVD2Yuyu8U02c/UgMREsl4ymuOWU5PzJjc690iecp4wb2C5'
               '2fJNyyfyffO/XoFawV3RW6BbsLZgdKXnyvpV0Kqlq3pX668uWj2+xm/NgbWEtWlrfyi0LiwvfLku'
               'Zl1PkVbRmqKx9X7rW4sVikXFNza4bKjbiNoo2Di4ae6mqk0fS3glF0utSytK32/mbr74lc1XlV99'
               '2pK0ZbDMoWzPVsxW4dbr29y3HShXLs8vH9sesr1zB2NHyY6XO5fsvFBhV1G3i7BLsktaGVzZXWVQ'
               'tbXqfXVK9UiNV017rWbtptrXu3m7r+zx2NNWp1VXWvdur2DvzXq/+s4Go4aKfZh9OfseNkY39n/N'
               '+rq5SaOptOnDfuF+6YGIA33Njs3NLZotZa1wq6R18mDCwcvfeH/T3cZsq2+nt5ceAockhx5/m/jt'
               '9cNBh3uPsI60fWf4XW0HtaOkE+pc3jnVldIl7Y7rHj4aeLS3x6Wn43vL7/cf0z1Wc1zleNkJwomi'
               'E59O5p+cPpV16unp5NNjvUt675yJPXOtL7xv8GzQ2fPnfM+d6ffsP3ne9fyxC84Xjl5kXey65HCp'
               'c8B+oOMH+x86Bh0GO4cch7ovO13uGZ43fOKK+5XTV72vnrsWcO3SyPyR4etR12/eSLghvcm7+ehW'
               '+q3nt3Nuz9xZcxd9t+Se0r2K+5r3G340/bFd6iA9Puo9OvBgwYM7Y9yxJz9l//R+vOgh+WHFhM5E'
               '8yPbR8cmfScvP174ePxJ1pOZp8U/K/9c+8zk2Xe/ePwyMBU7Nf5c9PzTr5tfqL/Y/9LuZe902PT9'
               'VxmvZl6XvFF/c+At623/u5h3EzO577HvKz+Yfuj5GPTx7qeMT59+A/eE8/vsbQFrAAAAIGNIUk0A'
               'AHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAAGYktHRAD/AP8A/6C9p5MAAAAJ'
               'cEhZcwAACxMAAAsTAQCanBgAABAySURBVGje7Vl5eFRFtv+dqnv79t6dhZCdNQKahJBAgLAEFNQZ'
               'xQWeEhFBYcQFV8DxOY5vfL43n+PnCuIyuAGCuIA7gygzgAIzBlnFD0GUrUMSkkB3J73dper9kU4I'
               'IaAz45u/pr7vdvftW1XnVP3O+Z1z6pK/dFT3ZstMs9xeHUICQhLaGkFCmOS3LKcVbdnbvHe7jn+3'
               'n6W5zytk3OXv38y5KTSHAYlT+w4JMJKqadpcpmEocUVNXd3QWMqDLZMYwd3aow0jUFyIg7888s0s'
               'X0lFNoBj/+rFqN40GOGmn9w/a8Zc1L76ZPu91i0b/rLRqP/kzVP/pWcj0fj/vxTPwAo079rS5TNm'
               'd2eF8rO+XbNj7xM2xgYRICXQ9kkghIUQX1zWPeMDRVd4QmHqdZLkyO2RltF+rjjBiENKCQnxnR7d'
               '7+5bqAjTPN9zQVkG0xwmGI+bjbVBozkU0nJ6WSLaDDMeFYnAwS4VKl26BdunVcBXOoL0xuPMaA4q'
               'jszcbtzl1cxIOKEfD9QrnhShpmaI0PZN7UbC/WlwFxSy6OHvVRBsanpmpOWbr0TZki+wbfqo02SU'
               'fXII2y7tifDnn5KjzwCPltY9xwieqHFk92yu/+RN+AYOzwcxnxk68V36hBtihxf85gw9pZTwDRoB'
               'M3iCW3oU0jCY6ksV3OlJgRB5Qo9LdDT4pC0zm42Is4OSeDdpxF0gzqHY9jXv3Nx8DgwJh46wH4z4'
               'Eo3YhwCEBIiBqEVY0QF252eMSDGBVUqbegAZ9zUc3NU+xZVTPQ6nL8NlWmkey0qHQj9ASEvquhE7'
               '/K0ZOXJAQAiXEY+RPSPLpqVk2OzdsuOhHZsbOmuzfVoFfING5gk9ASsWjZknG4yEsGJabm89UXPI'
               'MsInnczm0KQQdt+gkS2hHZtOAICnz/m9jZONscTxQJTZNG7Pyi/wDxpxeNv0UfHOMrZd2hO+wWOc'
               'MI2s0M7Nxx3dcxtAZDMj4X7OgqJQeM/WE+njJkaIU1pw0xoO4PAZu0YEX+mo3gREEseOJLjmYs78'
               'Ap8RPB5KGTqeEVezZdLUOw6SeuL78I4tFDl64Ej2pJkjpWUcbtq4Rk0ZMqbvya0bvu/ITqeGKQ0p'
               'mm3Y7NovN3mnzRmoERU3KMpqvPLYCQD4tGexfsoKKsb3/rSmboEkGjb+0O50AMiZctdV3O5YCiK1'
               'gwBq/00kAAhpmCFIa4cVi6449s6LK9z9S3xCWL06r4MpNtayd/sO/5ALu7n7FT3IVG0SOPe1z2mZ'
               'jZaeWFyzfMEjnsLyDCsRzWZcIRGPfZ0ybNwV3OGaT4xaEo11w1r27ykQZtw406IluGo3XAUDG9TU'
               '1M+JKQUiHvvPwPL5j+dMueNG7vQshJSuln07c41gE7MSsfTOm0fEeaKpdnfmpVUzSFHnSSlrAkuf'
               'GpM39Z7JpGmvAaR27RPEj/95ZVpG5dVvgbMLATARjz4cWL7gEU/h4BIrHgPodH1JUY3I3h3f5Ey5'
               'cwa3OxeCyCH0+MLA68/cmQSpgUlRfXFGtzuULmUyypNSHoGUEoAkQIDAATggYQdglwQPKTwX4LmK'
               'TZuQd9N9f5SGfmtg2fw3Os+XM+VOh39w5aPMpt0PKU0JuQ2W+S1ATgB9ifGe3O58OH/Gr+da8diE'
               'mjee3dg2Nm3MhFfAmE9KWUuK6mrZu23rueKAb9Coa4gpBQAYKXwQADCbowpSukAEaVnu5j1b9wE4'
               '2tX4nKo7+jC743GAPLDMeCv8ZEHIQ0RSA0gCMAFYADRAkrSszfGD352UYxAhgLfGHOd/502fWyT0'
               '2KyaFc+f7Cwn94a7XCmDxyxkNm12K5eJWljWii7j1xlKPrgQzd/uXGg0Ha8wQ00jmvduq7TikSVW'
               'LLLUjLSMtCLhchGPlolEotgMB0dKQ38TUoIY9zDNsTxnyp2zACCt8jIAQPdLqnzc7viS2bT7pWXu'
               'M8InCmKH91Uefe3x8dHvvxkr4tEyYeiLktbh4XbnuowrpvXroFJj8tvBbHb/jwVrKc0wAJGMMb7k'
               '3/qp55DZk28fmTdt7tq8afc+DwApQ8Z2mEAAEomOcwaWPb3SikZGWrGW4S37d5Vasegiaei79aa6'
               'S6xoS/nRxU9OAwC95tBkKxG7uY1JSFH/gzs8u7MnzRoMABmXTQEApF88OYsUe3UbQMLU1xuhk4MC'
               'bzy7pUiewYw4w5Nqfn8HAMgQNoa1vALe/aKrPgXnF0JYMCPNz9e8/WKkQ/d9ADbnTL1nF9fsjwIA'
               'dzj/6CupeLNp4+pw+tiJzJaZ+wKIFUHKJiPYVFn3/mv1rn4lAICmz1cnyt/fe7T6qgG35N84rxe4'
               'Mh5EipaauRZAz+Su7gXQB4CfFOU8AN+kVvwCJ7asOQtKFG2jMSLm6/xYxKM6d7rWE+MKAOROvbs6'
               'sGz+4vwZ9+PIq4+dFfxjbz13AgByp815n9m0KwFAGon/rflgSXvqKVVFr1k2/+Xsa279QfH43gZR'
               'GohyFV/K5pwpd15R88azazMnzuxvS0nfm6RrSxj6ksDSp2YOeXcnGjd8iK+JftyTOjZv/2IFjGlt'
               'qTu6QBkAapY98wdpmdVtoctTOORhAFBTUgcS59e1Wou5pO791+rtub0Q2bezfWz1VQMAAOF9OydB'
               'itYZOMvLue6uSwBAWtZHSd4HceW3AHBiyxp0u+Sas/lS5FSsIU/np9zuUKVlzWrrw2z2RVlXzSg6'
               'F0Cnhx9ktHtKp5h2fPUbKHltI4698+Jf9GBTibTMPycH2bjD+Une9DlPMcazpCUsaZm1IhGrCix9'
               'aiYAbJ1YArOpHj+J7jpxx9mR6dTM5uBD7ZOq2jgA4G7vH9oCphlqehkAVLuXPH0HnnZ5+5dR8K/r'
               'moWuL2ybgqnKaAAwI+EPIWVNK3hKad70eeuc/c63QZyZCycpzuyQEMgudpkFlj71mrTMtcl7VU3t'
               '9kXqmAmen4SSxDn3Y+dNlQCAundfDhxd/MQ4oetvtxkvKbZ7mcvz4NHFj6tHFz+RHVg2f6W3cPCP'
               'ilR+rsKtdtXLX+b/6oFWTBl3AFCZYru4lWOsZiKy595w76OQXRuGt3y0ELoeYJq9LXvpnzXpZl67'
               '6qW6nMm3TWRO92JifAApykXpFZcfEZa5KveGe3dDyjoprSiklASKSsvU24xPSnHWirVu8RMTMm+8'
               'bzdxPgBEPleP814+AUz+uQtaI9w0T3F5d3O78yEQaUxRL8q76b5DVjx6/bEVz21KHT0B4T1f/WtA'
               'Squ8rFu7sVlGfebEmUVtti70xHo1LaMaIOVcPAKJjZDiJIilgChL6gkOwKp564XqrIkzhzDNPonZ'
               'tAdI0fozxm7vXBsKPf6+FOKldoYwzfVn3TzAFInYFdzh/ArEfKSo12ZXzd4IKd/7p/Zh9OVo+vxj'
               'AEDe9LmrSFEvlULsMYINIxVf+jpizEeM5ytO98acqtl3H3r+dwv/KU8SpiEB4kneiCbroy6bI/+8'
               'OW3MKBOxZ7nm6N8hp99vRSNvM0UtPxtEUlgH9ca65Vp2z52tDCm9kk5F0dp3X4kAWJq81Mwrp/cn'
               'myONqaoKIcxEY+3BxnXvHsq7cd4qABxSxi0j/s651lezYuGB3Kn3Psg0bSEAKC7Pc2ZLONKWHZ7l'
               'nIC3G6NpnpYF9pz1IA4t+j2yr72tP3c43yPF1h+QgBQB5nB9Hdm/I9dVMPA94so4gBh3eZ/NnTZn'
               'iHmy8e66j5YG+857EgeemPv3gdS04SNdy8iZTYqtWMRa1te+92qsUxdX1pU39eNe/7XMpt3cmvHo'
               '7wRWPPdW3tS77+0QJxpqVixcDmD5ueTlTL6tOwFGe7yks7NI3QdLvm6zj8yJM4u07nlT82fcPxlE'
               'ha1eFftt7TuLDv2YlQaWPf1c7tR7zmN2x11SCBBnWZ1j2f9IiYeS9iIMYy0DnRCG8Xr9pyu/b+tT'
               '8uo62jljnMypmj2FO90vgMgLSIhE/AEr2Di/9uNlCQAJ1Zt+mZqacQuz2xe0xm/bNFt65sisSb+q'
               'OvDE3K2Z19+FuuULfhykrGtuzVEcjiclsbKkwoKrKQ/lTp/DScIJghtccRLjp/IKKSPSMt+LHthz'
               'fdJ7HB1qj8TfwRht0AgSUuZUzb6Q2bTfgJgfkDxZQHokyMcY94CfpkNcCvGD1Xzy9mMrX1rbxZxI'
               'FqOdgHrm7oxfTnn1+J/e2JVTdUc+gHnJJEEAwPxfXOvIvf7uO8FoBICEFFaIOLsm94Z7qlqplWp2'
               'zhh3a+4N9zzNbI57Wr1HhqxE7Jaa5Qve6iirfs0KHcCz2VWzv1ec7tdBlArGeqv+9OrcKXdMDSxf'
               'sPwneRJX1ctJUSefkelJACQlQBEIeVBaRh0gvpMS1RBiU92HS36wZ+bmuQaUmlJYB2CZ30HK3VKI'
               'tz2F5T1kPMq7SrggIZnd4eYu70FhmQ0khZSW9VLdR0v1vOlznyfV1q91mGytRqUASalLKY/CMAKA'
               '3C+l3AaJbcGt678BUYq7b2FvEEiYVlAKq6Z1LDYyTQt4i8r7iGjk1MsBCbTs2XrSM6C0hDQtIE1j'
               'F4gi0jIXAYA9LfNaptkf68qzpZCAsP7U7ZJrspnNfgsgIS1zi0jEbm7c8HG9u6CoN4RAR1lgDMG/'
               'fvaVv3zsYO7yPElcuTpZe3TvOgevGN97XY+ijz/rWdzYRXpOHb7PZvXkLRzc2ztweJm3qDyz9Whm'
               'ZF/fwApn2zhf6agy/9ALU895nFM6IsVfVtmnPdsrHub3Fg9PB8CYYnMzVXUrjJwAbJ3lA2De4qG9'
               'vEVDy3wlw3p5+l3Q3sE/uLL0NDllo4r9Qy9K6VKHslEpvkGjeravq6Sil39w5UVK670CQO3iYgDA'
               'nT612/hJvbKunlEJAP6yyvP9ZaPTz7Zef0mFN3X4xUMAIOvK6eXdJ0wf0vH5pz2LG9b1KFzNhozt'
               'RTRifO/PAvUvgGRl2DInqYy7SEqRRIUSUjZOLMja4K0PXWDp8RYQA3c4BSyLQIC0BDFFrQvt/lu8'
               'VbnREPEwiNnyLFNXmGpD8+7qwxIQ/vKxCFav7woghLZvhq+kIg1SeqQUEpBxUjQuDd1Gis0EAVJI'
               'gtCZiMeJVA3EmADAhGWCBOqav9122ul49o2/RmjDBwr3peaLaItgDheDsGrCe7Ym/OUXIlj9l44A'
               'IbTtC/gGVaRZsbib2TRAjzeEv90R9RYP6yOlsLo0VdMC4yojux1WSzguTVPnLncKwAOhnV/Eesz6'
               'Lxxe9MiZJUfx8BSdk/3txmCWHbIPIJFInoKYQsTcXFlBEpsuzki7mWxDxxasPFY/GqDhktD6hrCD'
               'MjEp1lYd3fueb+Cw/NCuvx35R1NTR1YPxGoPn8OTRiK0fdPPWqPY3G7oLS1dbNBQhHd/eaZ1l41G'
               'cNvn/7A8f+koDjCK7PvSNCJx+AaNQmjHF12f5hQOyQ/v2Xrknbzz59iIBrad6XSgCFUI8WZVdtZ3'
               '5C8b3T+oaQ1ITdfPCBdSAscOaymKln/yqw3b//3S++drvoEVduJqn2CK7yjS063W5IdOBRbGgP37'
               'vCkg+/8BldoYh+HwAs0AAAAASUVORK5CYII='
               )

def time_header():
    return datetime.now().strftime('[ %H:%M:%S ] ')


def interrupt_exit(signal, frame):
    print('\n\033[91mInterrupted by user. Exiting.\033[0m')
    sys.exit(1)


def dir_prep(d):
    if not isdir(d):
        try:
            makedirs(d)
        except:
            print('The output directory (' + d + ') could not be created. Exiting.')
            sys.exit(1)
    
    print('The output directory is set to: \033[93m' + d + '\033[0m')


def gen_html(title, h2g_summary, g2h_summary, h2g_images, g2h_images, html_outname):
    content = (
               '<!doctype html>\n'
               '<html>\n'
               '<head>\n'
               '<meta charset="utf-8" />\n'
               '<style>\n'
               'body {\n'
               '    background-color: #eeffff;\n'
               '    font-family: Verdana, Helvetica, sans-serif;\n'
               '    height: 100%;\n'
               '    margin: 0px;\n'
               '    text-align: center;\n'
               '}\n'
               '#container {\n'
               '    width: 100%;\n'
               '    min-width: 800px;\n'
               '    height: 100%;\n'
               '}\n'
               '#header, #footer {\n'
               '    display: inline-block;\n'
               '    width: 100%;\n'
               '    min-width: 800px;\n'
               '    padding: 0.3em 0px;\n'
               '    background-color: #eeeeee;\n'
               '    background-image: url("' + daynix_logo + '");\n'
               '    background-repeat: no-repeat;\n'
               '    background-position: 10px 50%;\n'
               '}\n'
               '#h2g {\n'
               '    width: 50%;\n'
               '    float: left;\n'
               '    height: auto !important;\n'
               '    height: 100%;\n'
               '    min-height: 100%;\n'
               '}\n'
               '#g2h {\n'
               '    background-color: #ffffee;\n'
               '    width: 50%;\n'
               '    float: right;\n'
               '    height: auto !important;\n'
               '    height: 100%;\n'
               '    min-height: 100%;\n'
               '}\n'
               '#missing {\n'
               '    position: relative;\n'
               '    width: 90%;\n'
               '    max-width: 1024px;\n'
               '    padding-bottom: 67.5%;\n'
               '    margin: 5px auto;\n'
               '    background-color: #ffcccc;\n'
               '    z-index: 10;\n'
               '}\n'
               '#missing > div {\n'
               '    position: absolute;\n'
               '    width: 100%;\n'
               '    padding: 1em;\n'
               '    z-index: 20;\n'
               '}\n'
               'img {\n'
               '    max-width: 90%;\n'
               '    margin: 5px auto;\n'
               '    display: block;\n'
               '}\n'
               'h1 {\n'
               '    margin-bottom: 0px;\n'
               '}\n'
               'h3, p {\n'
               '    margin: 0px;\n'
               '}\n'
               '</style>\n'
               '<title>Iperf Host &#8596; Guest Bandwidth and CPU Usage Report</title>\n'
               '</head>\n'
               '<body>\n'
               '<div id="header">\n'
               )
    content += '    <h3>' + title + '</h3>\n'
    content += (
                '</div>\n'
                '<div id="container">\n'
                '    <div id="h2g">\n'
                '        <h1>Host &#8594; Guest Results</h1>\n'
                '        <hr>\n'
                '        <h2>By Packet Size</h2>\n'
                )
    content += '        <img src="' + h2g_summary + '">\n'
    content += (
                '        <hr>\n'
                '        <h2>By Time</h2>\n'
                )
    for f in h2g_images:
        if f.split('.')[-1] == 'png':
            content += '        <img src="' + f + '">\n'
        else:
            content += (
                        '        <div id="missing"><div><h2>Packet size: '
                        + f +
                        '</h2><h3>(Host to Guest)</h3></br></br></br><h1>'
                        'Test failed to finish</h1></div></div>\n'
                        )
    content += (
                '    </div>\n'
                '    <div id="g2h">\n'
                '        <h1>Guest &#8594; Host Results</h1>\n'
                '        <hr>\n'
                '        <h2>By Packet Size</h2>\n'
                )
    content += '        <img src="' + g2h_summary + '">\n'
    content += (
                '        <hr>\n'
                '        <h2>By Time</h2>\n'
                )
    for f in g2h_images:
        if f.split('.')[-1] == 'png':
            content += '        <img src="' + f + '">\n'
        else:
            content += (
                        '        <div id="missing"><div><h2>Packet size: '
                        + f +
                        '</h2><h3>(Guest to host)</h3></br></br></br><h1>'
                        'Test failed to finish</h1></div></div>\n'
                        )
    content += (
                '    </div>\n'
                '</div>\n'
                '<div id="footer">\n'
                '    <p>&#169; Daynix Computing LTD</p>\n'
                '</div>\n'
                '</body>\n'
                '</html>\n'
                )
    with open(html_outname, 'w') as outfile:
        outfile.write(content)


def get_size_units_factor(num, rate=False):
    factor = 1.0
    if rate:
        s = 'b/s'
    else:
        s = 'B'

    for x in ['' + s, 'K' + s, 'M' + s, 'G' + s]:
        if num < 1024.0:
            return "%3.2f" % num, x, str(factor)

        num /= 1024.0
        factor *= 1024.0
    return "%3.2f" % num, 'T' + s, str(factor)


def get_round_size_name(i, gap = False):
    size_name = get_size_units_factor(i)
    if gap:
        return str(int(round(float(size_name[0])))) + ' ' + size_name[1]
    else:
        return str(int(round(float(size_name[0])))) + size_name[1]


def get_iperf_data_single(iperf_out):
    iperf_data = []
    with open(iperf_out, encoding='utf-8', errors='ignore') as inputfile:
        for line in inputfile:
            tmp_lst = line.strip().split(',')
            if (int(tmp_lst[-4]) > 0):
                date = datetime.strptime(tmp_lst[0], '%Y%m%d%H%M%S')
                if not iperf_data:
                    first_date = date

                time_from_start = float((date - first_date).total_seconds())
                rate = float(tmp_lst[-1])
                if (int(tmp_lst[-2]) < 0) or (rate < 0.0):
                    rate = np.nan

                iperf_data.append([ time_from_start, int(tmp_lst[-4]), rate ])

    iperf_data = np.array(iperf_data)
    bi_sorted_indices = np.lexsort((iperf_data[:,0], iperf_data[:,1]))
    iperf_data = iperf_data[bi_sorted_indices]
    num_conn = np.unique(iperf_data[:,1]).shape[0]
    #print(str(num_conn) + str(iperf_data.shape))
    iperf_data = iperf_data[:,[0,2]].reshape((num_conn, iperf_data.shape[0]/num_conn, 2))
    iperf_data = np.ma.masked_array(iperf_data, np.isnan(iperf_data))
    #iperf_mean = np.mean(iperf_data, axis=0)
    mean_times = np.mean(iperf_data[:,:,0], axis=0)
    #iperf_min = np.amin(iperf_data[:,:,1], axis=0).reshape(-1, 1)
    #iperf_max = np.amax(iperf_data[:,:,1], axis=0).reshape(-1, 1)
    #iperf_mean[:,0] = np.rint(iperf_mean[:,0])
    iperf_stdev = np.std(iperf_data[:,:,1], axis=0) * np.sqrt(num_conn)
    #return np.hstack((iperf_mean,iperf_stdev)).filled(np.nan)
    out_arr = np.vstack((mean_times, iperf_data[:,:,1].sum(axis=0), iperf_stdev)).filled(np.nan).T
    return out_arr, out_arr[:,1].mean(), out_arr[:,1].std()


def get_mpstat_data_single(mpstat_out):
    mpstat_data = []
    tmp_row = []
    time_interval = 0.0
    with open(mpstat_out) as inputfile:
        for line in inputfile:
            tmp_lst = line.split()
            if (not any('CPU' in s for s in tmp_lst)) and tmp_lst and ('Average' not in tmp_lst[0]):
                if any('all' in s for s in tmp_lst):
                    if tmp_row:
                        mpstat_data.append(tmp_row)

                    tmp_row = []
                else:
                    tmp_row.append(float(tmp_lst[-1]))

                if not time_interval:
                    time = datetime.strptime(tmp_lst[0] + tmp_lst[1], '%I:%M:%S%p')
                    if not mpstat_data:
                        first_time = time

                    time_interval = float((time - first_time).total_seconds())

    mpstat_data.append(tmp_row)
    mpstat_data = np.array(mpstat_data)
    num_measurements, num_cpu = mpstat_data.shape
    times = np.arange(0, num_measurements * time_interval, time_interval)
    mpstat_data = (1 - mpstat_data / 100) / num_cpu
    tot_cpu_usage = mpstat_data.sum(axis=1)
    core_stdev = np.std(mpstat_data, axis=1) * np.sqrt(num_cpu)
    #mpstat_mean = np.mean(mpstat_data, axis=1)
    #mpstat_min = np.min(mpstat_data, axis=1)
    #mpstat_max = np.max(mpstat_data, axis=1)
    out_arr = np.vstack((times, tot_cpu_usage, core_stdev)).T
    return out_arr, out_arr[:,1].mean(), out_arr[:,1].std()


def export_single_data(data_processed, data_outname):
    np.savetxt(data_outname, data_processed, fmt='%g', header='TimeStamp(s) Sum Stdev')


def write_gp(gp_outname, net_dat_file, proc_dat_file, img_file, net_rate,
             plot_type = 'singlesize', direction = 'h2g', packet_size = 0.0):
    try:
        net_rate, rate_units, rate_factor = get_size_units_factor(net_rate, rate=True)
        rate_format = ''
    except:
        net_rate = '???'
        rate_units = 'b/s'
        rate_factor = '1.0'
        rate_format = 'set format y "%.1tx10^%T"'

    packet_size = get_round_size_name(packet_size, gap = True)
    if plot_type == 'singlesize':
        plot_title = 'Packet size: ' + packet_size + ', Av. rate: ' + net_rate + ' ' + rate_units
        x_title = 'Time (s)'
        xtic_explicit = ''
        labels_above_points = ''
        log2_scale = ''
        rotate_xtics = ''
    else:
        plot_title = 'Bandwidth \\\\& CPU usage for different packet sizes'
        x_title = 'Packet size'
        xtic_explicit = ':xtic($1 < 1024.0 ? sprintf("%.0fB", $1) : ($1 < 1048576.0 ? sprintf("%.0fKB", $1/1024.0) : sprintf("%.0fMB", $1/1048576.0)))'
        labels_above_points = ('     "" using 1:($2/' + rate_factor + '):(sprintf("%.2f ' + rate_units + '",'
                               ' $2/' + rate_factor + ')) with labels offset 0.9,1.0 rotate by 90 font ",12" notitle, \\\n')
        log2_scale = 'set logscale x 2\n'
        rotate_xtics = 'set xtics rotate by -30\n'

    if direction == 'h2g':
        plot_subtitle = '(Host to Guest)'
    else:
        plot_subtitle = '(Guest to Host)'

    content = (
               'set terminal pngcairo nocrop enhanced size 1024,768 font "Verdana,15"\n'
               'set output "' + img_file +'"\n'
               '\n'
               'set title "{/=20 ' + plot_title + '}\\n\\n{/=18 ' + plot_subtitle + '}"\n'
               + rate_format + '\n'
               'set xlabel "' + x_title + '"\n'
               'set ylabel "Bandwidth (' + rate_units + ')"\n'
               'set ytics nomirror\n'
               'set y2label "CPU busy time fraction"\n'
               'set y2tics nomirror\n'
               'set y2range [0:1]\n'
               'set key bmargin center horizontal box samplen 1 width -1\n'
               'set bmargin 4.6\n'
               + log2_scale + rotate_xtics +
               '\n'
               'set style fill transparent solid 0.2 noborder\n'
               'plot "' + net_dat_file + '" using 1:($2/' + rate_factor + '-$3/' + rate_factor + '):'
                     '($2/' + rate_factor + '+$3/' + rate_factor + ') with filledcurves lc rgb "blue" notitle, \\\n'
               '     "" using 1:($2/' + rate_factor + ')' + xtic_explicit + ' with points'
                     ' pt 2 ps 1.5 lw 3 lc rgb "blue" title "Mean tot. BW", \\\n'
               + labels_above_points +
               '     "' + proc_dat_file + '" using 1:($2-$3):($2+$3) with filledcurves lc rgb "red" axes x1y2 notitle, \\\n'
               '     "" using 1:2 with points pt 1 ps 1.5 lw 3 lc rgb "red" axes x1y2 title "Mean tot. CPU"\n'
              )
    with open(gp_outname, 'w') as outfile:
        outfile.write(content)


def run_client(server_addr, runtime, p_size, queues, export_dir, timestamp, credsfile = False):
    repetitions, mod = divmod(runtime, 10)
    if not mod:
        runtime -= 1

    size_name = get_round_size_name(p_size)
    iperf_args =  ' -c ' + server_addr + ' -t ' + str(runtime) + ' -i 10 -l ' + str(p_size) + ' -P ' + str(queues) + ' -y C'
    if credsfile:
        iperf_command = 'winexe -A ' + credsfile + ' //' + remote_addr + ' "' + remote_iperf + iperf_args + '"'
        basename = join(export_dir, timestamp, timestamp) + '_g2h_' + size_name
    else:
        iperf_command = local_iperf + iperf_args
        basename = join(export_dir, timestamp, timestamp) + '_h2g_' + size_name

    commands = [
                iperf_command + ' > ' + basename + '_iperf.dat',
                'mpstat -P ALL 10 ' + str(repetitions) + ' > ' + basename + '_mpstat.dat',
               ]
    print(time_header() + 'Running ' + size_name + ' test. (Duration: '
          + str(timedelta(seconds = repetitions * 10 + mod)) + ')')
    iperf_proc = Popen(commands[0], shell=True)
    mpstat_proc = Popen(commands[1], shell=True)
    mpstat_proc.wait()
    waitcount = 0
    while iperf_proc.poll() == None:
        if waitcount < 1:
            print(time_header() + '\033[93mThe Iperf test is not over yet.\033[0m Waiting for 10 more seconds...')
            sleep(10)
            waitcount += 1
        else:
            iperf_proc.kill()
            sleep(2)

    if not iperf_proc.poll():
        print(time_header() + '\033[92mThe ' + size_name + ' test finished.\033[0m Waiting for 10 seconds.')
        sleep(10)
        return True
    else:
        print(time_header() + '\033[91mThe Iperf test failed to finish.\033[0m Skipping in 10 seconds.')
        sleep(10)
        return False


def stop_server(server_addr = False, credsfile = False):
    if credsfile and server_addr:
        iperf_stop_command = 'winexe -A ' + credsfile + ' //' + server_addr + ' "taskkill /im ' + remote_iperf.split('\\')[-1] + ' /f"'
        print('Stopping previous remote server instances... \033[92m[Please ignore an ERROR message if present in the line below]\033[0m')
    else:
        iperf_stop_command = 'killall -9 ' + local_iperf
        print('Stopping previous local server instances...')

    p = Popen(iperf_stop_command, shell=True)
    p.wait()
    sleep(10)


def run_server(server_addr = False, credsfile = False):
    iperf_args =  ' -s'
    if credsfile and server_addr:
        iperf_command = 'winexe -A ' + credsfile + ' //' + server_addr + ' "' + remote_iperf + iperf_args + '"'
        rem_loc = 'remote'
    else:
        iperf_command = local_iperf + iperf_args
        rem_loc = 'local'
        error_note = ''

    print('Starting ' + rem_loc + ' server...')
    p = Popen(iperf_command, shell=True)
    sleep(10)


def run_tests(remote_addr, local_addr, runtime, p_sizes, queues, timestamp, credsfile, test_title, export_dir):
    dir_prep(join(export_dir, timestamp))
    dir_time = join(export_dir, timestamp, timestamp)
    total_time = str(timedelta(seconds = 2 * len(p_sizes) * (runtime + 10) + 60))
    print(time_header() + '\033[92mStarting tests.\033[0m Expected total run time: ' + total_time)
    h2g_iperf_tot = []
    h2g_mpstat_tot = []
    g2h_iperf_tot = []
    g2h_mpstat_tot = []
    h2g_images = []
    g2h_images = []
    stop_server()
    stop_server(remote_addr, credsfile)
    run_server(remote_addr, credsfile)
    for p in p_sizes:
        finished = run_client(remote_addr, runtime, p, queues, export_dir, timestamp, credsfile = False)
        size_name = get_round_size_name(p)
        basename = dir_time + '_h2g_' + size_name
        if finished:
            print('Parsing results...')
            iperf_array, tot_iperf_mean, tot_iperf_stdev = get_iperf_data_single(basename + '_iperf.dat')
            h2g_iperf_tot.append([ p, tot_iperf_mean, tot_iperf_stdev ])
            mpstat_array, tot_mpstat_mean, tot_mpstat_stdev = get_mpstat_data_single(basename + '_mpstat.dat')
            h2g_mpstat_tot.append([ p, tot_mpstat_mean, tot_mpstat_stdev ])
            export_single_data(iperf_array, basename + '_iperf_processed.dat')
            export_single_data(mpstat_array, basename + '_mpstat_processed.dat')
            write_gp(basename + '.plt', basename + '_iperf_processed.dat', basename + '_mpstat_processed.dat', basename + '.png',
                     tot_iperf_mean, plot_type = 'singlesize', direction = 'h2g', packet_size = p)
            print('Plotting...')
            pr = Popen(gnuplot_bin + ' ' + basename + '.plt', shell=True)
            pr.wait()
            h2g_images.append(timestamp + '_h2g_' + size_name + '.png')
        else:
            h2g_images.append(get_round_size_name(p, gap = True))

    stop_server(remote_addr, credsfile)
    print('Plotting host --> guest summary...')
    np.savetxt(dir_time + '_h2g_iperf_summary.dat', h2g_iperf_tot, fmt='%g', header='PacketSize(b) BW Stdev')
    np.savetxt(dir_time + '_h2g_mpstat_summary.dat', h2g_mpstat_tot, fmt='%g', header='PacketSize(b) Frac Stdev')
    write_gp(dir_time + '_h2g_summary.plt', dir_time + '_h2g_iperf_summary.dat', dir_time + '_h2g_mpstat_summary.dat',
             dir_time + '_h2g_summary.png', tot_iperf_mean, plot_type = 'multisize', direction = 'h2g', packet_size = np.mean(p_sizes))
    pr = Popen(gnuplot_bin + ' ' + dir_time + '_h2g_summary.plt', shell=True)
    pr.wait()
    run_server()
    for p in p_sizes:
        finished = run_client(local_addr, runtime, p, queues, export_dir, timestamp, credsfile)
        size_name = get_round_size_name(p)
        basename = dir_time + '_g2h_' + size_name
        if finished:
            print('Parsing results...')
            iperf_array, tot_iperf_mean, tot_iperf_stdev = get_iperf_data_single(basename + '_iperf.dat')
            g2h_iperf_tot.append([ p, tot_iperf_mean, tot_iperf_stdev ])
            mpstat_array, tot_mpstat_mean, tot_mpstat_stdev = get_mpstat_data_single(basename + '_mpstat.dat')
            g2h_mpstat_tot.append([ p, tot_mpstat_mean, tot_mpstat_stdev ])
            export_single_data(iperf_array, basename + '_iperf_processed.dat')
            export_single_data(mpstat_array, basename + '_mpstat_processed.dat')
            write_gp(basename + '.plt', basename + '_iperf_processed.dat', basename + '_mpstat_processed.dat', basename + '.png',
                     tot_iperf_mean, plot_type = 'singlesize', direction = 'g2h', packet_size = p)
            print('Plotting...')
            pr = Popen(gnuplot_bin + ' ' + basename + '.plt', shell=True)
            pr.wait()
            g2h_images.append(timestamp + '_g2h_' + size_name + '.png')
        else:
            g2h_images.append(get_round_size_name(p, gap = True))

    stop_server()
    print('Plotting guest --> host summary...')
    np.savetxt(dir_time + '_g2h_iperf_summary.dat', g2h_iperf_tot, fmt='%g', header='PacketSize(b) BW Stdev')
    np.savetxt(dir_time + '_g2h_mpstat_summary.dat', g2h_mpstat_tot, fmt='%g', header='PacketSize(b) Frac Stdev')
    write_gp(dir_time + '_g2h_summary.plt', dir_time + '_g2h_iperf_summary.dat', dir_time + '_g2h_mpstat_summary.dat',
             dir_time + '_g2h_summary.png', tot_iperf_mean, plot_type = 'multisize', direction = 'g2h', packet_size = np.mean(p_sizes))
    pr = Popen(gnuplot_bin + ' ' + dir_time + '_g2h_summary.plt', shell=True)
    pr.wait()
    print('Exporting html...')
    gen_html(test_title, timestamp + '_h2g_summary.png', timestamp + '_g2h_summary.png', h2g_images, g2h_images, dir_time + '.html')


if __name__ == "__main__":
    export_dir = 'out'
    remote_addr = '10.0.1.114'
    local_addr = '10.0.0.157'
    remote_iperf = 'C:\iperf\iperf.exe'
    local_iperf = 'iperf'
    gnuplot_bin = 'gnuplot'
    test_range = [2**x for x in range(5,17)]  #32B --> 64KB
    run_duration = 300
    streams = 1
    creds = 'creds.dat'
    title = 'Test Results (5 min per run)'
    # Interrupt handling
    signal.signal(signal.SIGINT, interrupt_exit)
    # Run tests
    run_tests(remote_addr, local_addr, run_duration, test_range, streams, rundate, creds, title, export_dir)
