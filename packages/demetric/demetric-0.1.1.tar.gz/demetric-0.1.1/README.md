# Demetric

> Simple and composable metric tracking and logging for ML

```python
import demetric as dm

exp = dm.Experiment(id='gpt2-3', base_path='runs', meta={
  'model': 'gpt2',
  'batch_size': 128
})

exp.log('loss', value=loss, step=step)
exp.log('accuracy', value=acc, step=step)


fig, ax = exp.plot('loss')
fig2, ax2 = exp.plot_summary()
```