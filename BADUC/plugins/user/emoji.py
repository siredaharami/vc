from pyrogram import *
from pyrogram.types import *
from BADUC import SUDOERS
from BADUC.core.clients import app
from BADUC.core.command import *
from BADUC.database.basic import edit_or_reply, get_text


rtext = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]


remoji = [
    "⁭\n                    💖\n                  💖💖\n               💖💖💖\n            💖💖 💖💖\n          💖💖    💖💖\n        💖💖       💖💖\n      💖💖💖💖💖💖\n     💖💖💖💖💖💖💖\n   💖💖                 💖💖\n  💖💖                    💖💖\n💖💖                       💖💖\n",
    "⁭\n💗💗💗💗💗💗💗\n💗💗💗💗💗💗💗💗\n💗💗                     💗💗\n💗💗                     💗💗\n💗💗💗💗💗💗💗💗\n💗💗💗💗💗💗💗💗\n💗💗                     💗💗\n💗💗                     💗💗\n💗💗💗💗💗💗💗💗\n💗💗💗💗💗💗💗\n",
    "⁭\n          💛💛💛💛💛💛\n     💛💛💛💛💛💛💛💛\n   💛💛                      💛💛\n 💛💛\n💛💛\n💛💛\n 💛💛\n   💛💛                      💛💛\n     💛💛💛💛💛💛💛💛\n         💛💛💛💛💛💛\n",
    "⁭\n💙💙💙💙💙💙💙\n💙💙💙💙💙💙💙💙\n💙💙                      💙💙\n💙💙                         💙💙\n💙💙                         💙💙\n💙💙                         💙💙\n💙💙                         💙💙\n💙💙                      💙💙\n💙💙💙💙💙💙💙💙\n💙💙💙💙💙💙💙\n",
    "⁭\n💟💟💟💟💟💟💟💟\n💟💟💟💟💟💟💟💟\n💟💟\n💟💟\n💟💟💟💟💟💟\n💟💟💟💟💟💟\n💟💟\n💟💟\n💟💟💟💟💟💟💟💟\n💟💟💟💟💟💟💟💟\n",
    "⁭\n💚💚💚💚💚💚💚💚\n💚💚💚💚💚💚💚💚\n💚💚\n💚💚\n💚💚💚💚💚💚\n💚💚💚💚💚💚\n💚💚\n💚💚\n💚💚\n💚💚\n",
    "⁭\n          💜💜💜💜💜💜\n     💜💜💜💜💜💜💜💜\n   💜💜                     💜💜\n 💜💜\n💜💜                💜💜💜💜\n💜💜                💜💜💜💜\n 💜💜                        💜💜\n   💜💜                      💜💜\n     💜💜💜💜💜💜💜💜\n          💜💜💜💜💜💜\n",
    "⁭\n💖💖                        💖💖\n💖💖                        💖💖\n💖💖                        💖💖\n💖💖                        💖💖\n💖💖💖💖💖💖💖💖💖\n💖💖💖💖💖💖💖💖💖\n💖💖                        💖💖\n💖💖                        💖💖\n💖💖                        💖💖\n💖💖                        💖💖\n",
    "⁭\n💗💗💗💗💗💗\n💗💗💗💗💗💗\n          💗💗\n          💗💗\n          💗💗\n          💗💗\n          💗💗\n          💗💗\n💗💗💗💗💗💗\n💗💗💗💗💗💗\n",
    "⁭\n         💛💛💛💛💛💛\n         💛💛💛💛💛💛\n                  💛💛\n                  💛💛\n                  💛💛\n                  💛💛\n💛💛          💛💛\n  💛💛       💛💛\n   💛💛💛💛💛\n      💛💛💛💛\n",
    "⁭\n💙💙                  💙💙\n💙💙             💙💙\n💙💙        💙💙\n💙💙   💙💙\n💙💙💙💙\n💙💙 💙💙\n💙💙     💙💙\n💙💙         💙💙\n💙💙              💙💙\n💙💙                   💙💙\n",
    "⁭\n💟💟\n💟💟\n💟💟\n💟💟\n💟💟\n💟💟\n💟💟\n💟💟\n💟💟💟💟💟💟💟💟\n💟💟💟💟💟💟💟💟\n",
    "⁭\n💚💚                              💚💚\n💚💚💚                      💚💚💚\n💚💚💚💚            💚💚💚💚\n💚💚    💚💚    💚💚    💚💚\n💚💚        💚💚💚        💚💚\n💚💚             💚             💚💚\n💚💚                              💚💚\n💚💚                              💚💚\n💚💚                              💚💚\n💚💚                              💚💚\n",
    "⁭\n💜💜                           💜💜\n💜💜💜                       💜💜\n💜💜💜💜                 💜💜\n💜💜  💜💜               💜💜\n💜💜     💜💜            💜💜\n💜💜         💜💜        💜💜\n💜💜             💜💜    💜💜\n💜💜                 💜💜💜💜\n💜💜                     💜💜💜\n💜💜                          💜💜\n",
    "⁭\n           💖💖💖💖💖\n     💖💖💖💖💖💖💖\n   💖💖                   💖💖\n 💖💖                       💖💖\n💖💖                         💖💖\n💖💖                         💖💖\n 💖💖                       💖💖\n   💖💖                   💖💖\n      💖💖💖💖💖💖💖\n            💖💖💖💖💖\n",
    "⁭\n💗💗💗💗💗💗💗\n💗💗💗💗💗💗💗💗\n💗💗                     💗💗\n💗💗                     💗💗\n💗💗💗💗💗💗💗💗\n💗💗💗💗💗💗💗\n💗💗\n💗💗\n💗💗\n💗💗\n",
    "⁭\n           💛💛💛💛💛\n      💛💛💛💛💛💛💛\n   💛💛                    💛💛\n 💛💛                        💛💛\n💛💛                           💛💛\n💛💛              💛💛     💛💛\n 💛💛               💛💛 💛💛\n   💛💛                   💛💛\n      💛💛💛💛💛💛💛💛\n           💛💛💛💛💛   💛💛\n",
    "⁭\n💙💙💙💙💙💙💙\n💙💙💙💙💙💙💙💙\n💙💙                     💙💙\n💙💙                     💙💙\n💙💙💙💙💙💙💙💙\n💙💙💙💙💙💙💙\n💙💙    💙💙\n💙💙         💙💙\n💙💙              💙💙\n💙💙                  💙💙\n",
    "⁭\n       💟💟💟💟💟\n  💟💟💟💟💟💟💟\n  💟💟                 💟💟\n💟💟\n  💟💟💟💟💟💟\n      💟💟💟💟💟💟\n                            💟💟\n💟💟                 💟💟\n  💟💟💟💟💟💟💟\n       💟💟💟💟💟\n",
    "⁭\n💚💚💚💚💚💚💚💚\n💚💚💚💚💚💚💚💚\n               💚💚\n               💚💚\n               💚💚\n               💚💚\n               💚💚\n               💚💚\n               💚💚\n",
    "⁭\n💜💜                      💜💜\n💜💜                      💜💜\n💜💜                      💜💜\n💜💜                      💜💜\n💜💜                      💜💜\n💜💜                      💜💜\n💜💜                      💜💜\n  💜💜                  💜💜\n      💜💜💜💜💜💜\n            💜💜💜💜\n",
    "⁭\n💖💖                              💖💖\n  💖💖                          💖💖\n    💖💖                      💖💖\n      💖💖                  💖💖\n         💖💖              💖💖\n           💖💖         💖💖\n             💖💖     💖💖\n               💖💖 💖💖\n                  💖💖💖\n                       💖\n",
    "⁭\n💗💗                               💗💗\n💗💗                               💗💗\n💗💗                               💗💗\n💗💗                               💗💗\n💗💗              💗            💗💗\n 💗💗           💗💗          💗💗\n 💗💗        💗💗💗       💗💗\n  💗💗   💗💗  💗💗   💗💗\n   💗💗💗💗      💗💗💗💗\n    💗💗💗             💗💗💗\n",
    "⁭\n💛💛                    💛💛\n   💛💛              💛💛\n      💛💛        💛💛\n         💛💛  💛💛\n            💛💛💛\n            💛💛💛\n         💛💛 💛💛\n      💛💛       💛💛\n   💛💛             💛💛\n💛💛                   💛💛\n",
    "⁭\n💙💙                    💙💙\n   💙💙              💙💙\n      💙💙        💙💙\n         💙💙  💙💙\n            💙💙💙\n              💙💙\n              💙💙\n              💙💙\n              💙💙\n              💙💙\n",
    "⁭\n 💟💟💟💟💟💟💟\n 💟💟💟💟💟💟💟\n                       💟💟\n                   💟💟\n               💟💟\n           💟💟\n       💟💟\n   💟💟\n💟💟💟💟💟💟💟\n💟💟💟💟💟💟💟\n",
    "⁭\n       💗💗💗💗\n   💗💗💗💗💗💗\n💗💗               💗💗\n💗💗               💗💗\n💗💗               💗💗\n💗💗               💗💗\n💗💗               💗💗\n💗💗               💗💗\n   💗💗💗💗💗💗\n        💗💗💗💗\n",
    "⁭\n          💙💙\n     💙💙💙\n💙💙 💙💙\n          💙💙\n          💙💙\n          💙💙\n          💙💙\n          💙💙\n     💙💙💙💙\n     💙💙💙💙\n",
    "⁭\n    💟💟💟💟💟\n  💟💟💟💟💟💟\n💟💟          💟💟\n                💟💟\n             💟💟\n          💟💟\n       💟💟\n    💟💟\n  💟💟💟💟💟💟\n  💟💟💟💟💟💟\n",
    "⁭\n     💛💛💛💛\n  💛💛💛💛💛\n💛💛         💛💛\n                   💛💛\n            💛💛💛\n            💛💛💛\n                   💛💛\n💛💛         💛💛\n  💛💛💛💛💛\n     💛💛💛💛\n",
    "⁭\n                         💖💖\n                    💖💖💖\n              💖💖 💖💖\n          💖💖     💖💖\n     💖💖          💖💖\n💖💖               💖💖\n💖💖💖💖💖💖💖💖💖\n💖💖💖💖💖💖💖💖💖\n                         💖💖\n                         💖💖\n",
    "⁭\n💚💚💚💚💚💚\n💚💚💚💚💚💚\n💚💚\n 💚💚💚💚💚\n   💚💚💚💚💚\n                    💚💚\n                    💚💚\n💚💚          💚💚\n  💚💚💚💚💚\n     💚💚💚💚\n",
    "⁭\n        💜💜💜💜\n    💜💜💜💜💜\n💜💜\n\n💜💜\n💜💜💜💜💜💜\n💜💜💜💜💜💜💜\n💜💜               💜💜\n💜💜               💜💜\n    💜💜💜💜💜💜\n        💜💜💜💜\n",
    "⁭\n💗💗💗💗💗💗💗\n💗💗💗💗💗💗💗\n                      💗💗\n                     💗💗\n                   💗💗\n                 💗💗\n               💗💗\n             💗💗\n           💗💗\n         💗💗\n",
    "⁭\n        💙💙💙💙\n   💙💙💙💙💙💙\n💙💙               💙💙\n💙💙               💙💙\n   💙💙💙💙💙💙\n   💙💙💙💙💙💙\n💙💙               💙💙\n💙💙               💙💙\n   💙💙💙💙💙💙\n        💙💙💙💙\n",
    "⁭\n        💟💟💟💟\n   💟💟💟💟💟💟\n💟💟               💟💟\n💟💟               💟💟\n 💟💟💟💟💟💟💟\n      💟💟💟💟💟💟\n                         💟💟\n                        💟💟\n  💟💟💟💟💟💟\n       💟💟💟💟\n",
]


rtemoji = [
    "⁭\n                    {cj}\n                  {cj}{cj}\n               {cj}{cj}{cj}\n            {cj}{cj} {cj}{cj}\n          {cj}{cj}    {cj}{cj}\n        {cj}{cj}       {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}\n     {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                 {cj}{cj}\n  {cj}{cj}                    {cj}{cj}\n{cj}{cj}                       {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n          {cj}{cj}{cj}{cj}{cj}{cj}\n     {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                      {cj}{cj}\n {cj}{cj}\n{cj}{cj}\n{cj}{cj}\n {cj}{cj}\n   {cj}{cj}                      {cj}{cj}\n     {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n         {cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n",
    "⁭\n          {cj}{cj}{cj}{cj}{cj}{cj}\n     {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                     {cj}{cj}\n {cj}{cj}\n{cj}{cj}                {cj}{cj}{cj}{cj}\n{cj}{cj}                {cj}{cj}{cj}{cj}\n {cj}{cj}                        {cj}{cj}\n   {cj}{cj}                      {cj}{cj}\n     {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n          {cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}                        {cj}{cj}\n{cj}{cj}                        {cj}{cj}\n{cj}{cj}                        {cj}{cj}\n{cj}{cj}                        {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                        {cj}{cj}\n{cj}{cj}                        {cj}{cj}\n{cj}{cj}                        {cj}{cj}\n{cj}{cj}                        {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n         {cj}{cj}{cj}{cj}{cj}{cj}\n         {cj}{cj}{cj}{cj}{cj}{cj}\n                  {cj}{cj}\n                  {cj}{cj}\n                  {cj}{cj}\n                  {cj}{cj}\n{cj}{cj}          {cj}{cj}\n  {cj}{cj}       {cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}                  {cj}{cj}\n{cj}{cj}             {cj}{cj}\n{cj}{cj}        {cj}{cj}\n{cj}{cj}   {cj}{cj}\n{cj}{cj}{cj}{cj}\n{cj}{cj} {cj}{cj}\n{cj}{cj}     {cj}{cj}\n{cj}{cj}         {cj}{cj}\n{cj}{cj}              {cj}{cj}\n{cj}{cj}                   {cj}{cj}\n",
    "⁭\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}                              {cj}{cj}\n{cj}{cj}{cj}                      {cj}{cj}{cj}\n{cj}{cj}{cj}{cj}            {cj}{cj}{cj}{cj}\n{cj}{cj}    {cj}{cj}    {cj}{cj}    {cj}{cj}\n{cj}{cj}        {cj}{cj}{cj}        {cj}{cj}\n{cj}{cj}             {cj}             {cj}{cj}\n{cj}{cj}                              {cj}{cj}\n{cj}{cj}                              {cj}{cj}\n{cj}{cj}                              {cj}{cj}\n{cj}{cj}                              {cj}{cj}\n",
    "⁭\n{cj}{cj}                           {cj}{cj}\n{cj}{cj}{cj}                       {cj}{cj}\n{cj}{cj}{cj}{cj}                 {cj}{cj}\n{cj}{cj}  {cj}{cj}               {cj}{cj}\n{cj}{cj}     {cj}{cj}            {cj}{cj}\n{cj}{cj}         {cj}{cj}        {cj}{cj}\n{cj}{cj}             {cj}{cj}    {cj}{cj}\n{cj}{cj}                 {cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}{cj}\n{cj}{cj}                          {cj}{cj}\n",
    "⁭\n           {cj}{cj}{cj}{cj}{cj}\n     {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n {cj}{cj}                       {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n{cj}{cj}                         {cj}{cj}\n {cj}{cj}                       {cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n            {cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n{cj}{cj}\n",
    "⁭\n           {cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}                    {cj}{cj}\n {cj}{cj}                        {cj}{cj}\n{cj}{cj}                           {cj}{cj}\n{cj}{cj}              {cj}{cj}     {cj}{cj}\n {cj}{cj}               {cj}{cj} {cj}{cj}\n   {cj}{cj}                   {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n           {cj}{cj}{cj}{cj}{cj}   {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}                     {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}    {cj}{cj}\n{cj}{cj}         {cj}{cj}\n{cj}{cj}              {cj}{cj}\n{cj}{cj}                  {cj}{cj}\n",
    "⁭\n       {cj}{cj}{cj}{cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n  {cj}{cj}                 {cj}{cj}\n{cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}\n                            {cj}{cj}\n{cj}{cj}                 {cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n       {cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n               {cj}{cj}\n               {cj}{cj}\n               {cj}{cj}\n               {cj}{cj}\n               {cj}{cj}\n               {cj}{cj}\n               {cj}{cj}\n",
    "⁭\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n{cj}{cj}                      {cj}{cj}\n  {cj}{cj}                  {cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}\n            {cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}                              {cj}{cj}\n  {cj}{cj}                          {cj}{cj}\n    {cj}{cj}                      {cj}{cj}\n      {cj}{cj}                  {cj}{cj}\n         {cj}{cj}              {cj}{cj}\n           {cj}{cj}         {cj}{cj}\n             {cj}{cj}     {cj}{cj}\n               {cj}{cj} {cj}{cj}\n                  {cj}{cj}{cj}\n                       {cj}\n",
    "⁭\n{cj}{cj}                               {cj}{cj}\n{cj}{cj}                               {cj}{cj}\n{cj}{cj}                               {cj}{cj}\n{cj}{cj}                               {cj}{cj}\n{cj}{cj}              {cj}            {cj}{cj}\n {cj}{cj}           {cj}{cj}          {cj}{cj}\n {cj}{cj}        {cj}{cj}{cj}       {cj}{cj}\n  {cj}{cj}   {cj}{cj}  {cj}{cj}   {cj}{cj}\n   {cj}{cj}{cj}{cj}      {cj}{cj}{cj}{cj}\n    {cj}{cj}{cj}             {cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}                    {cj}{cj}\n   {cj}{cj}              {cj}{cj}\n      {cj}{cj}        {cj}{cj}\n         {cj}{cj}  {cj}{cj}\n            {cj}{cj}{cj}\n            {cj}{cj}{cj}\n         {cj}{cj} {cj}{cj}\n      {cj}{cj}       {cj}{cj}\n   {cj}{cj}             {cj}{cj}\n{cj}{cj}                   {cj}{cj}\n",
    "⁭\n{cj}{cj}                    {cj}{cj}\n   {cj}{cj}              {cj}{cj}\n      {cj}{cj}        {cj}{cj}\n         {cj}{cj}  {cj}{cj}\n            {cj}{cj}{cj}\n              {cj}{cj}\n              {cj}{cj}\n              {cj}{cj}\n              {cj}{cj}\n              {cj}{cj}\n",
    "⁭\n {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n                       {cj}{cj}\n                   {cj}{cj}\n               {cj}{cj}\n           {cj}{cj}\n       {cj}{cj}\n   {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n       {cj}{cj}{cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}{cj}\n        {cj}{cj}{cj}{cj}\n",
    "⁭\n          {cj}{cj}\n     {cj}{cj}{cj}\n{cj}{cj} {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n          {cj}{cj}\n     {cj}{cj}{cj}{cj}\n     {cj}{cj}{cj}{cj}\n",
    "⁭\n    {cj}{cj}{cj}{cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}          {cj}{cj}\n                {cj}{cj}\n             {cj}{cj}\n          {cj}{cj}\n       {cj}{cj}\n    {cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}{cj}\n",
    "⁭\n     {cj}{cj}{cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}\n{cj}{cj}         {cj}{cj}\n                   {cj}{cj}\n            {cj}{cj}{cj}\n            {cj}{cj}{cj}\n                   {cj}{cj}\n{cj}{cj}         {cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}\n     {cj}{cj}{cj}{cj}\n",
    "⁭\n                         {cj}{cj}\n                    {cj}{cj}{cj}\n              {cj}{cj} {cj}{cj}\n          {cj}{cj}     {cj}{cj}\n     {cj}{cj}          {cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n                         {cj}{cj}\n                         {cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n {cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}\n                    {cj}{cj}\n                    {cj}{cj}\n{cj}{cj}          {cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}\n     {cj}{cj}{cj}{cj}\n",
    "⁭\n        {cj}{cj}{cj}{cj}\n    {cj}{cj}{cj}{cj}{cj}\n{cj}{cj}\n\n{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n    {cj}{cj}{cj}{cj}{cj}{cj}\n        {cj}{cj}{cj}{cj}\n",
    "⁭\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}{cj}{cj}{cj}{cj}{cj}\n                      {cj}{cj}\n                     {cj}{cj}\n                   {cj}{cj}\n                 {cj}{cj}\n               {cj}{cj}\n             {cj}{cj}\n           {cj}{cj}\n         {cj}{cj}\n",
    "⁭\n        {cj}{cj}{cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}{cj}\n        {cj}{cj}{cj}{cj}\n",
    "⁭\n        {cj}{cj}{cj}{cj}\n   {cj}{cj}{cj}{cj}{cj}{cj}\n{cj}{cj}               {cj}{cj}\n{cj}{cj}               {cj}{cj}\n {cj}{cj}{cj}{cj}{cj}{cj}{cj}\n      {cj}{cj}{cj}{cj}{cj}{cj}\n                         {cj}{cj}\n                        {cj}{cj}\n  {cj}{cj}{cj}{cj}{cj}{cj}\n       {cj}{cj}{cj}{cj}\n",
]


@app.on_message(bad(["emoji"]) & (filters.me | filters.user(SUDOERS)))
async def emoji(client: Client, message: Message):
    op = await edit_or_reply(message, "`Emojifying the text..`")
    args = get_text(message)
    if not args:
        if not message.reply_to_message:
           return await ok.edit("__What am I Supposed to do with this idiot, Give me a text.__")
        if not message.reply_to_message.text:
           return await ok.edit("__What am I Supposed to do with this idiot, Give me a text.__")
    args = args or message.reply_to_message.text
    
    result = ""
    for a in args:
        a = a.lower()
        if a in rtext:
            char = remoji[rtext.index(a)]
            result += char
        else:
            result += a
    await op.edit(result)
    

@app.on_message(bad(["lemoji"]) & (filters.me | filters.user(SUDOERS)))
async def cmoji(client: Client, message: Message):
    op = await edit_or_reply(message, "`Emojifying the text..`")
    args = get_text(message)
    if not args:
        if not message.reply_to_message:
           return await ok.edit("__What am I Supposed to do with this idiot, Give me a text.__")
        if not message.reply_to_message.text:
           return await ok.edit("__What am I Supposed to do with this idiot, Give me a text.__")
    args = args or message.reply_to_message.text
    try:
        emoji, arg = args.split(" ", 1)
    except Exception:
        arg = args
        emoji = "❤️"
    result = ""
    for a in arg:
        a = a.lower()
        if a in rtext:
            char = rtemoji[rtext.index(a)].format(cj=emoji)
            result += char
        else:
            result += a
    await op.edit(result)
    


__NAME__ = "Eᴍᴏᴊɪ"
__MENU__ = """
`.emoji` - **.emoji (name)**
`.love` - **.cmoji (emoji or text) (name)**

**Alternate Command:** '`whois`'
"""
