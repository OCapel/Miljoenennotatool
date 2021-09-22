# Helm Chart

This functionality is in development and is subject to change. The code is provided as-is with no warranties.

## Usage

[Helm](https://helm.sh) must be installed to use the charts.
Please refer to Helm's [documentation](https://helm.sh/docs/) to get started.

Once Helm is set up properly, install the Helm chart as follows:

Please inspect `values.yaml` for possible configuration options or you will
receive an error when trying to install the Helm chart.

First, make the desired changes to `values.yaml`

Next, run the following command:

```console
helm install -n dsh-prod -f ./coalitieakkoordentool/values.yaml coalitieakkoordentool ./coalitieakkoordentool
```

Optionally, you can then run `helm test coalitieakkoordentool` to test the deployment(s).

Note: when applicable add `-n <namespace>` to run the commands in namespace.