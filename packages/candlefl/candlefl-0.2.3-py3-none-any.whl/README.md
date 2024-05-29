
## Table of Contents

- [Key Features](#features)
- [Installation](#installation)
- [Examples and Usage](#examples-and-usage)
- [Available Models](#available-models)
- [Available Datasets](#available-datasets)
- [Contributing](#contributing)
- [Citation](#citation)

## Features

- Python 3.6+ support. Built using ```torch-1.10.1```, ```torchvision-0.11.2```, and ```pytorch-lightning-1.5.7```.
- Customizable implementations for state-of-the-art deep learning [models](#available-models) which can be trained in federated or non-federated settings.
- Supports finetuning of the pre-trained deep learning models, allowing for faster training using transfer learning.
- PyTorch LightningDataModule wrappers for the most commonly used [datasets](#available-datasets) to reduce the boilerplate code before experiments.
- Built using the bottom-up approach for the datamodules and models which ensures abstractions while allowing for customization.
- Provides implementation of the federated learning (FL) samplers, aggregators, and wrappers, to prototype FL experiments on-the-go.
- Backwards compatible with the PyTorch LightningDataModule, LightningModule, loggers, and DevOps tools.
- More details about the examples and usage can be found [below](#examples-and-usage).

## Installation
### Stable Release
As of now, ```candlefl``` is available on PyPI and can be installed using the following command in your terminal:
```
$ pip install candlefl
```
This is the preferred method to install ```candlefl``` with the most stable release.
If you don't have [pip](https://pip.pypa.io/en/stable/) installed, this [Python installation guide](http://docs.python-guide.org/en/latest/starting/installation/) can guide you through the process.

## Examples and Usage
Although ```candlefl``` is primarily built for quick prototyping of federated learning experiments, the models, datasets, and abstractions can also speed up the non-federated learning experiments. In this section, we will explore examples and usages under both the settings.

### Non-Federated Learning
The following steps should be followed on a high-level to train a non-federated learning experiment. We are using the ```EMNIST (MNIST)``` dataset and ```densenet121``` for this example.

1. Import the relevant modules.
	```python
	from candlefl.datamodules.emnist import EMNISTDataModule
	from candlefl.models.wrapper.emnist import MNISTEMNIST
	```

	```python
	import pytorch_lightning as pl
	from pytorch_lightning.loggers import TensorBoardLogger
	from pytorch_lightning.callbacks import (
		ModelCheckpoint,
		LearningRateMonitor,
		DeviceStatsMonitor,
		ModelSummary,
		ProgressBar,
		...
	)
	```
	For more details, view the full list of PyTorch Lightning [callbacks](https://pytorch-lightning.readthedocs.io/en/stable/extensions/callbacks.html#callback) and [loggers](https://pytorch-lightning.readthedocs.io/en/latest/common/loggers.html#loggers) on the official website.
2. Setup the PyTorch Lightning trainer.
	```python
	trainer = pl.Trainer(
		...
		logger=[
			TensorBoardLogger(
				name=experiment_name,
				save_dir=os.path.join(checkpoint_save_path, experiment_name),
			)
		],
		callbacks=[
			ModelCheckpoint(save_weights_only=True, mode="max", monitor="val_acc"),
			LearningRateMonitor("epoch"),
			DeviceStatsMonitor(),
			ModelSummary(),
			ProgressBar(),
		],
		...
	)
	```
	More details about the PyTorch Lightning [Trainer API](https://pytorch-lightning.readthedocs.io/en/latest/common/trainer.html#) can be found on their official website.

3. Prepare the dataset using the wrappers provided by ```candlefl.datamodules```.
	```python
	datamodule = EMNISTDataModule(dataset_name="mnist")
	datamodule.prepare_data()
	datamodule.setup()
	```

4. Initialize the model using the wrappers provided by ```candlefl.models.wrappers```.
	```python
	# check if the model can be loaded from a given checkpoint
	if (checkpoint_load_path) and os.path.isfile(checkpoint_load_path):
		model = MNISTEMNIST(
			"densenet121", "adam", {"lr": 0.001}
			).load_from_checkpoint(checkpoint_load_path)
	else:
		pl.seed_everything(42)
		model = MNISTEMNIST("densenet121", "adam", {"lr": 0.001})
		trainer.fit(model, datamodule.train_dataloader(), datamodule.val_dataloader())
	```

5. Collect the results.
	```python
	val_result = trainer.test(
		model, test_dataloaders=datamodule.val_dataloader(), verbose=True
	)
	test_result = trainer.test(
		model, test_dataloaders=datamodule.test_dataloader(), verbose=True
	)
	```

6. The corresponding files for the experiment (model checkpoints and logger metadata) will be stored at ```default_root_dir``` argument given to the PyTorch Lightning ```Trainer``` object in Step 2. For this experiment, we use the [Tensorboard](https://www.tensorflow.org/tensorboard) logger. To view the logs (and related plots and metrics), go to the ```default_root_dir``` path and find the Tensorboard log files. Upload the files to the Tensorboard Development portal following the instructions [here](https://tensorboard.dev/#get-started). Once the log files are uploaded, a unique url to your experiment will be generated which can be shared with ease! An example can be found [here](https://tensorboard.dev/experiment/Q1tw19FySLSjLN6CW5DaUw/).

7. Note that, ```candlefl``` is compatible with all the loggers supported by PyTorch Lightning. More information about the PyTorch Lightning loggers can be found [here](https://pytorch-lightning.readthedocs.io/en/latest/common/loggers.html#loggers).


### Federated Learning
The following steps should be followed on a high-level to train a federated learning experiment.

1. Pick a dataset and use the ```datamodules``` to create federated data shards with iid or non-iid distribution.
	```python
	def get_datamodule() -> EMNISTDataModule:
		datamodule: EMNISTDataModule = EMNISTDataModule(
			dataset_name=SUPPORTED_DATASETS_TYPE.MNIST, train_batch_size=10
		)
		datamodule.prepare_data()
		datamodule.setup()
		return datamodule

    agent_data_shard_map = get_agent_data_shard_map().federated_iid_dataloader(
        num_workers=fl_params.num_agents,
        workers_batch_size=fl_params.local_train_batch_size,
    )
	```
2. Use the TorchFL ```agents``` module and the  ```models``` module to initialize the global model, agents, and distribute their models.
	```python
	def initialize_agents(
		fl_params: FLParams, agent_data_shard_map: Dict[int, DataLoader]
	) -> List[V1Agent]:
		"""Initialize agents."""
		agents = []
		for agent_id in range(fl_params.num_agents):
			agent = V1Agent(
				id=agent_id,
				model=MNISTEMNIST(
					model_name=EMNIST_MODELS_ENUM.MOBILENETV3SMALL,
					optimizer_name=OPTIMIZERS_TYPE.ADAM,
					optimizer_hparams={"lr": 0.001},
					model_hparams={"pre_trained": True, "feature_extract": True},
					fl_hparams=fl_params,
				),
				data_shard=agent_data_shard_map[agent_id],
			)
			agents.append(agent)
		return agents

	global_model = MNISTEMNIST(
        model_name=EMNIST_MODELS_ENUM.MOBILENETV3SMALL,
        optimizer_name=OPTIMIZERS_TYPE.ADAM,
        optimizer_hparams={"lr": 0.001},
        model_hparams={"pre_trained": True, "feature_extract": True},
        fl_hparams=fl_params,
    )

	all_agents = initialize_agents(fl_params, agent_data_shard_map)
	```
3. Initiliaze an ```FLParam``` object with the desired FL hyperparameters and pass it on to the ```Entrypoint``` object which will abstract the training.
	```python
    fl_params = FLParams(
        experiment_name="iid_mnist_fedavg_10_agents_5_sampled_50_epochs_mobilenetv3small_latest",
        num_agents=10,
        global_epochs=10,
        local_epochs=2,
        sampling_ratio=0.5,
    )
    entrypoint = Entrypoint(
        global_model=global_model,
        global_datamodule=get_agent_data_shard_map(),
        fl_hparams=fl_params,
        agents=all_agents,
        aggregator=FedAvgAggregator(all_agents=all_agents),
        sampler=RandomSampler(all_agents=all_agents),
    )
    entrypoint.run()
	```


## Available Models
For the initial release, ```candlefl``` will only support state-of-the-art computer vision models. The following table summarizes the available models, support for pre-training, and the possibility of feature-extracting. Please note that the models have been tested with all the available datasets. Therefore, the link to the tests will be provided in the next section.

## Available Datasets
Following datasets have been wrapped inside a ```LightningDataModule``` and made available for the initial release of ```candlefl```. To add a new dataset, check the source code in ```candlefl.datamodules```, add tests, and create a PR with ```Features``` tag.

## Contributing
Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

### Types of Contributions
#### Report Bugs

If you are reporting a bug, please include:
- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

#### Fix Bugs
Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

#### Implement Features
Look through the GitHub issues for features. Anything tagged with "enhancement", "help wanted", "feature" is open to whoever wants to implement it.

#### Write Documentation
```candlefl``` could always use more documentation, whether as part of the official candlefl docs, in docstrings, or even on the web in blog posts, articles, and such.

#### Submit Feedback
If you are proposing a feature:
- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome :)

### Get Started
Ready to contribute? Here's how to set up candlefl for local development.
1. Fork the candlefl repo on GitHub.

2. Clone your fork locally:
	```
	$ git clone git@github.com:<your_username_here>/candlefl.git
	```

3. Install Poetry to manage dependencies and virtual environments from https://python-poetry.org/docs/.

4. Install the project dependencies using:
	```
	$ poetry install
	```

5. To add a new dependency to the project, use:
	```
	$ poetry add <dependency_name>
	```

6. Create a branch for local development:
	```
	$ git checkout -b name-of-your-bugfix-or-feature
	```
	Now you can make your changes locally and maintain them on your own branch.

7. When you're done making changes, check that your changes pass the tests:
	```
	$ poetry run pytest tests
	```
	If you want to run a specific test file, use:
	```
	$ poetry pytest <path-to-the-file>
	```
	If your changes are not covered by the tests, please add tests.

8. The pre-commit hooks will be run before every commit. If you want to run them manually, use:
	```
	$ pre-commit run --all
	```

9. Commit your changes and push your branch to GitHub:
	```
	$ git add --all
	$ git commit -m "Your detailed description of your changes."
	$ git push origin <name-of-your-bugfix-or-feature>
	```
10. Submit a pull request through the Github web interface.
11. Once the pull request has been submitted, the continuous integration pipelines on Github Actions will be triggered. Ensure that all of them pass before one of the maintainers can review the request.

### Pull Request Guidelines
Before you submit a pull request, check that it meets these guidelines:
1. The pull request should include tests.
	- Try adding new test cases for new features or enhancements and make changes to the CI pipelines accordingly.
	- Modify the existing tests (if required) for the bug fixes.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in ```README.md```.
3. The pull request should pass all the existing CI pipelines (Github Actions) and the new/modified workflows should be added as required.

