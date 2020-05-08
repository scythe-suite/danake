export DANAKE_VERSION="0.3.0-beta"

export DANAKE_CONFS="$(realpath -eL $DANAKE_HOME/../confs)"

export DANAKE_CONTEXT=$(docker context inspect -f '{{.Name}}')
export DANAKE_MANAGER_IP=$(docker node inspect self -f '{{.ManagerStatus.Addr}}' | cut -f1 -d:)

if [ ! -r "$DANAKE_CONFS/danake-config.sh" ]; then
  echo "danake: missing user confs '$DANAKE_CONFS/danake-config.sh'" >&2
  exit 1
fi
source "$DANAKE_CONFS/danake-config.sh"

if [ -z $DANAKE_DEBUG ]; then
  export DANAKE_REGISTRY="scythesuitedanake"
else
  export DANAKE_REGISTRY="127.0.0.1:5000"
fi

