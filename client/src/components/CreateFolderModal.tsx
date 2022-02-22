import {Button, Input, Modal} from "antd";
import {useForm} from "react-hook-form";
import {Api} from "../utils/Api";

interface Props {
    visible: boolean;
    onClose: () => void;
}

export function CreateFolderModal({visible, onClose}: Props) {
    const api = new Api();
    const {register, handleSubmit} = useForm();

    const onSubmit = (data: any) => {
        api.createFolder(data.folderName)
    };

    return <Modal
        visible={visible}
        onCancel={onClose}
        title="Create Folder"
        footer={[
            <Button onClick={onClose}>
                Return
            </Button>,
            <Button type="primary" htmlType="submit" onClick={handleSubmit(onSubmit)}>
                Submit
            </Button>
        ]}
    >
        <form>
            <h3>Folder name</h3>
            <Input className="w-full" type="text" {...register("folderName")} />
        </form>
    </Modal>
}