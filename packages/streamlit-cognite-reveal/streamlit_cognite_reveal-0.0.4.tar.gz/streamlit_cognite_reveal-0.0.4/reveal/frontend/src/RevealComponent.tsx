import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode, useEffect, useMemo, useState } from "react"
import {
  RevealCanvas,
  AxisGizmo,
  RevealContext,
  SceneContainer,
  useClickedNodeData,
  RevealToolbar,
  AssetStylingGroup,
  useSceneDefaultCamera,
} from "@cognite/reveal-react-components"
import { CogniteClient } from "@cognite/sdk"
import { DefaultNodeAppearance } from "@cognite/reveal"

interface StState {
  lastClickedAsset: number | null
}

interface StStateProps {
  state: StState
  setState: (state: StState) => void
}

interface StClientConfig {
  // TODO: fix a way to call back to Python to generate a new token
  token: string
  project: string
  baseUrl: string
}


const AssetClickedHandler = ({setLastClickedAsset}: { setLastClickedAsset: (assetId: number) => void}) => {
  const clicked = useClickedNodeData();
  useEffect(() => {
    if (clicked && clicked.assetMappingResult && clicked.assetMappingResult.assetIds.length > 0) {
      setLastClickedAsset(clicked.assetMappingResult.assetIds[0]);
      // setSelectedAssetIds(clicked.assetMappingResult.assetIds)
    }  
  }, [clicked, setLastClickedAsset]);
  return <></>
};

const LoadDefaultCamera =  ({sceneExternalId, sceneSpace}: {sceneExternalId: string; sceneSpace: string}) => {
  const loadDefaultCamera = useSceneDefaultCamera(sceneExternalId, sceneSpace);
  loadDefaultCamera.fitCameraToSceneDefault();
  return <></>
}

const RevealComponent = ({
  clientConfig,
  sceneExternalId,
  sceneSpace,
  selectedAssetIdsArg
}: {
  clientConfig: StClientConfig
  sceneExternalId: string
  sceneSpace: string
  selectedAssetIdsArg: number[]
}) => {
  const defaultAssetStyling: AssetStylingGroup = {
    assetIds: [],
    style: {
      cad: DefaultNodeAppearance.Highlighted
    }
  };
  const [sdk, setSdk] = useState<CogniteClient | null>(null)
  const [selectedAssetIds, setSelectedAssetIds] = useState(selectedAssetIdsArg)
  const [styling, setStyling] = useState<AssetStylingGroup>(defaultAssetStyling);
  
  useEffect(() => {
    Streamlit.setFrameHeight(500)
  })

  useEffect(() => {
    const newSdk = new CogniteClient({
      project: clientConfig.project,
      baseUrl: clientConfig.baseUrl,
      appId: "streamlit-reveal-component",
      getToken: async () => {
        return clientConfig.token
      },
    })
    
    setSdk(newSdk)
  }, [clientConfig])

  useEffect(() => {
    Streamlit.setFrameHeight(500)
  })

  useEffect(() => {
    setSelectedAssetIds(selectedAssetIdsArg)
  }, [selectedAssetIdsArg])
  
  useEffect(() => {
    const assetStyling: AssetStylingGroup = {
      assetIds: selectedAssetIds,
      style: {
        cad: DefaultNodeAppearance.Highlighted
      }
    };
    setStyling(assetStyling)
  }, [selectedAssetIds])

  const [lastClickedAsset, setLastClickedAsset] = useState<number | null>(null);
  useMemo(() => {
    const state: StState = { lastClickedAsset };
    console.log(state);
    Streamlit.setComponentValue(state);
  }, [lastClickedAsset])

  return sdk === null ? (
    <>Loading ...</>
  ) : (
    <RevealContext viewerOptions={{useFlexibleCameraManager: true}} sdk={sdk}>
      <RevealCanvas>
        <RevealToolbar />
        <AxisGizmo />
        <SceneContainer
          sceneExternalId={sceneExternalId}
          sceneSpaceId={sceneSpace}
          instanceStyling={[styling]}
        />
        <LoadDefaultCamera sceneExternalId={sceneExternalId} sceneSpace={sceneSpace} />

        <AssetClickedHandler setLastClickedAsset={setLastClickedAsset} />
      </RevealCanvas>
    </RevealContext>
  )
}

class StreamlitComponent extends StreamlitComponentBase<StState> {

  public render = (): ReactNode => {
    const config: StClientConfig = this.props.args["client_config"]
    const selectedAssetIds: number[] = this.props.args["selected_asset_ids"] ?? []
    const sceneExternalId: string = this.props.args["scene_external_id"]
    const space: string = this.props.args["scene_space"]

    return (
      <RevealComponent 
        sceneExternalId={sceneExternalId}
        sceneSpace={space}
        clientConfig={config}
        selectedAssetIdsArg={selectedAssetIds}
      />
    )
  }
}

export default withStreamlitConnection(StreamlitComponent)
