
<h1 align="center">ALbedo ⚛️</h1>
<p>
  <a href="https://pypi.org/project/ALbedo/0.6896/" target="_blank">
  </a>
</p>

<h3 align="center"><span style="color:#FFC0CB">Your one-stop destination to utilize Active Learning Sampling methods with just one line of code.</span></h3>

<h4 align="center">
A Python library meant to simplify your life by providing you with popular active-learning sampling methods on image classification. You can train your models from scratch by tweaking a few values. Or if you want to try out pre-trained model like ResNet50, EfficientNetVB6, VGG19, etc., don't worry! This library has got you covered. From Bayesian optimization for least and high-confidence parameter tuning to margin sampling, you can try it out with just one simple command.
</h4>

<h4 align="center">____________________________________________________________________________</h4>

<dl>
  <dt><span style="color:#FFC0CB">How to import the library?</span></dt>
    <dd>Just run the following command on your terminal or online coding interface.
</dd>
</dl>

```
pip install ALbedo
```


<dl>
  <dt><span style="color:#FFC0CB">An example use case:</span>
    <dd>This will use the default values for the class object, as mentioned in the original code.
</dd>
</dl>

```python
from ALbedo import Classification

classifier=Classification(validation_split=0.4,early_stopping_patience=20)
```

<dl>
  <dt><span style="color:#FFC0CB">or,</span>
</dl>

```python
from ALbedo import Sampling

sampling=Sampling("mixedbayes","cifar10",first_data_samples=5000)
sampling.initial_training()
history_data=sampling.get_iterations()
```

This will use the Bayesian optimization method to find the optimal coefficient for highest confidence and least confidence samples.


<dl>
  <dt><span style="color:#FFC0CB">or,</span>
</dl>

```python
sampling=Sampling(file_input_params=True, filepath="parameters.txt")
sampling.model_params()
```

If you intend to use a file to input the parameters for the model sampling, this will help you out. Only the mentioned parameters will be tuned. The other parameters will be default values. Please look at the sample [parameters.txt] file for format clarifications.



<dl>
  <dt><span style="color:#FFC0CB">or, download pretrained models with your desired specifications!</span>
</dl>

```python
from ALbedo import PretrainedModel

pretrained=PretrainedModel(model_type="resnet50", dataset="cifar10", samplingtype="leastconfidence")
model=pretrained.get_model()
```

<h4 align="center">____________________________________________________________________________</h4>


This library is being actively updated and new features are being added frequently. New datasets and pre-trained models will be updated soon. Any bugs detected will be fixed asap.

Feel free to share your feedback! I would really appreciate it! ❤️️

